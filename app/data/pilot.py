"""SQL-backed scoped reads; no business record mutation capability."""

from datetime import UTC, date, datetime
from uuid import uuid4
import json
import logging
from functools import wraps
from pathlib import Path

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.data.models import (
    ApplicationUser, Assessment, AssessmentElement, AssessmentVersion, Assignment,
    AuditEvent, Employee, ProcessGrouping, RoleAssignment, Signature, Team,
)
from app.domain import AssessmentState, is_overdue
from app.services.contracts import AssessmentQueryScope, RoleScopeRecord
from app.services.pilot import (
    PilotAccessError, PilotDetail, PilotRow, PilotUnavailableError, PilotVersion, effective_scope,
)

def read_boundary(method):
    @wraps(method)
    def wrapped(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except (SQLAlchemyError, RuntimeError, OSError) as error:
            logging.getLogger(__name__).exception("Local pilot read dependency failed")
            raise PilotUnavailableError("The local demo is unavailable. Check setup and the server log.") from error
    return wrapped


class SqlPilotReader:
    def __init__(self, factory: sessionmaker[Session], as_of: date) -> None:
        self.factory = factory
        self.as_of = as_of

    def _ready(self) -> None:
        from app.data.demo import DEMO_VERSION

        bind = self.factory.kw["bind"]
        path = Path(bind.url.database).resolve()
        marker = path.with_suffix(path.suffix + ".synthetic-demo.json")
        try:
            manifest = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise RuntimeError("Run explicit init-demo before browsing the pilot.") from error
        if not path.is_file() or manifest != {
            "dataset": DEMO_VERSION, "database": str(path), "as_of": self.as_of.isoformat()
        }:
            raise RuntimeError("Unknown or incompatible demo database.")

    def _scope(self, session: Session, user_id: str, purpose: str, reference: str) -> AssessmentQueryScope:
        user = session.get(ApplicationUser, user_id)
        if user is None:
            raise PilotAccessError(401, "A configured synthetic identity is required.")
        if not user.is_active:
            self._audit(session, user_id, "Denied", None, "", "")
            raise PilotAccessError(403, "Access is not permitted.")
        roles = tuple(RoleScopeRecord(
            id=r.id, user_id=r.user_id, role=r.role_name, starts_at=r.starts_at,
            ends_at=r.ends_at, team_id=r.team_id, assessment_id=r.assessment_id,
            configuration_scope=r.configuration_scope,
        ) for r in session.scalars(select(RoleAssignment).where(RoleAssignment.user_id == user_id)))
        scope = effective_scope(user.id, user.employee_id, roles,
                                datetime.combine(self.as_of, datetime.min.time(), UTC))
        if scope.diagnostic and (not purpose.strip() or not reference.strip()):
            self._audit(session, user_id, "Denied", None, "", "")
            raise PilotAccessError(403, "Diagnostic purpose and support reference are required.")
        if len(purpose) > 200 or len(reference) > 128:
            raise PilotAccessError(400, "Diagnostic fields exceed their allowed length.")
        return scope

    @staticmethod
    def _statement(scope: AssessmentQueryScope):
        condition = or_(
            and_(Assignment.employee_id == scope.own_employee_id,
                 Assessment.id.in_(scope.own_assessment_ids)),
            Assignment.team_id.in_(scope.team_ids),
            and_(Assignment.assessor_id == scope.employee_id,
                 Assessment.id.in_(scope.assessor_assessment_ids)),
            and_(Assignment.technical_supervisor_id == scope.employee_id,
                 Assessment.id.in_(scope.technical_supervisor_assessment_ids)),
            Assignment.configuration_version_snapshot.in_(scope.configuration_versions),
        )
        return (select(Assessment, Assignment)
                .join(Assignment, Assessment.assignment_id == Assignment.id)
                .where(True if scope.diagnostic else condition)
                .order_by(Assignment.due_date, Assessment.id))

    def _row(self, session: Session, assessment: Assessment, assignment: Assignment,
             diagnostic: bool = False) -> PilotRow:
        employee = session.get(Employee, assignment.employee_id)
        team = session.get(Team, assignment.team_id)
        grouping = session.get(ProcessGrouping, assignment.process_grouping_id)
        if employee is None or team is None or grouping is None:
            raise RuntimeError("Pilot record has missing relationships.")
        return PilotRow(assessment.id, "Record status (diagnostic)" if diagnostic else employee.display_label, team.display_label,
                        grouping.display_label, assessment.lifecycle_state,
                        assignment.due_date, is_overdue(
                            due_date=assignment.due_date, as_of=self.as_of,
                            active=assessment.lifecycle_state != AssessmentState.FINALIZED.value))

    @staticmethod
    def _audit(session: Session, user_id: str, outcome: str, record_id: str | None,
               purpose: str, reference: str) -> None:
        request_id = uuid4().hex
        session.add(AuditEvent(
            id=f"UI-AUDIT-{request_id}", actor_user_id=user_id,
            action="diagnostic_read" if purpose else "pilot_read",
            entity_type="assessment" if record_id else "report",
            entity_id=record_id or "pilot_status", assessment_id=record_id,
            observed_at=datetime.now(UTC), outcome=outcome,
            request_identity=request_id, correlation_id=request_id,
            change_summary="Local pilot scoped read",
            support_purpose=purpose.strip() or None,
            support_reference=reference.strip() or None,
        ))
        session.commit()

    @read_boundary
    def list_rows(self, user_id: str, *, purpose: str = "", reference: str = "") -> tuple[PilotRow, ...]:
        self._ready()
        with self.factory() as session:
            scope = self._scope(session, user_id, purpose, reference)
            records = session.execute(self._statement(scope)).all()
            rows = tuple(self._row(session, a, assignment, scope.diagnostic) for a, assignment in records)
            if not rows:
                self._audit(session, user_id, "Denied", None, purpose, reference)
            for row in rows:
                self._audit(session, user_id, "Succeeded", row.id, purpose, reference)
            return rows

    @read_boundary
    def detail(self, user_id: str, record_id: str, *, purpose: str = "", reference: str = "") -> PilotDetail:
        self._ready()
        with self.factory() as session:
            scope = self._scope(session, user_id, purpose, reference)
            found = session.execute(self._statement(scope).where(Assessment.id == record_id)).first()
            if found is None:
                self._audit(session, user_id, "Denied", None, purpose, reference)
                raise PilotAccessError(404, "Record not found or not visible.")
            assessment, assignment = found
            row = self._row(session, assessment, assignment, scope.diagnostic)
            if scope.diagnostic:
                self._audit(session, user_id, "Succeeded", assessment.id, purpose, reference)
                return PilotDetail(row, (), (), diagnostic=True)
            participants = []
            for label, key in (
                ("Testing Personnel", assignment.employee_id),
                ("Assigned Team Lead", assignment.assigned_team_lead_id),
                ("Assessor", assignment.assessor_id),
                ("Technical Supervisor", assignment.technical_supervisor_id),
            ):
                employee = session.get(Employee, key)
                if employee is None:
                    raise RuntimeError("Pilot participant is unavailable.")
                participants.append((label, employee.display_label))
            versions = []
            for v in session.scalars(select(AssessmentVersion).where(
                    AssessmentVersion.assessment_id == assessment.id).order_by(AssessmentVersion.version_number)):
                elements = tuple(session.scalars(select(AssessmentElement).where(
                    AssessmentElement.assessment_version_id == v.id).order_by(AssessmentElement.element_ref)))
                signatures = tuple(session.scalars(select(Signature.signature_role).where(
                    Signature.assessment_version_id == v.id).order_by(Signature.signed_at)))
                versions.append(PilotVersion(v.version_number, v.assessment_context,
                    v.assessment_method, v.protocol_outcome,
                    "; ".join(e.evidence for e in elements),
                    v.followup_description or "Follow-up description missing in this issued version.",
                    v.is_locked, signatures))
            self._audit(session, user_id, "Succeeded", assessment.id, purpose, reference)
            return PilotDetail(row, tuple(participants), tuple(versions))
