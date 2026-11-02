from datetime import UTC, date, datetime

from app.domain import RejectionCode
from app.services import Actor,RoleScopeRecord
from tests.integration.test_workflow_service import advance, make_service


def test_roles_are_scoped_and_platform_diagnostic_requires_purpose():
    service,factory=make_service();advance(service)
    denied=service.begin_assessment(Actor("SYN-OUT-001"),assessment_id="SYN-ASM-001",
        request_id="denied",correlation_id="safe",expected_version=5)
    assert denied.code is RejectionCode.NOT_FOUND_OR_NOT_VISIBLE
    assert service.list_visible_assessments(Actor("SYN-OUT-001"),as_of=date(2027,2,20),request_id="out-read",correlation_id="out-read").items==()
    assert service.list_visible_assessments(Actor("SYN-PLAT-001"),as_of=date(2027,2,20),request_id="plat-denied",correlation_id="plat-denied").items==()
    rows=service.list_visible_assessments(Actor("SYN-PLAT-001"),as_of=date(2027,2,20),
        request_id="plat-read",correlation_id="plat-read",purpose="Synthetic support investigation",support_reference="SYN-TICKET-001")
    assert len(rows.items)==1
    assert any(a.request_id=="denied" and a.outcome=="Denied" for a in factory.store.audits)
    diagnostic=[a for a in factory.store.audits if a.request_id=="plat-read"]
    assert len(diagnostic)==1 and diagnostic[0].support_reference=="SYN-TICKET-001"


def test_non_author_roles_cannot_begin_or_sign():
    service,factory=make_service();advance(service)
    for index,user in enumerate(("SYN-EMP-001","SYN-LEAD-001","SYN-TS-001","SYN-ADM-001","SYN-PLAT-001")):
        result=service.begin_assessment(Actor(user),assessment_id="SYN-ASM-001",
            request_id=f"matrix-{index}",correlation_id=f"matrix-{index}",expected_version=5)
        expected=RejectionCode.FORBIDDEN if user=="SYN-PLAT-001" else RejectionCode.NOT_FOUND_OR_NOT_VISIBLE
        assert result.code is expected
    assert sum(a.outcome=="Denied" and a.request_id.startswith("matrix-") for a in factory.store.audits)==5


def test_each_approved_scope_sees_only_the_synthetic_record():
    service,_=make_service();advance(service)
    for user in ("SYN-EMP-001","SYN-LEAD-001","SYN-ASR-001","SYN-TS-001","SYN-ADM-001"):
        rows=service.list_visible_assessments(Actor(user),as_of=date(2027,2,20),
            request_id=f"read-{user}",correlation_id=f"read-{user}")
        assert len(rows.items)==1 and rows.items[0].assessment_id=="SYN-ASM-001"


def test_query_port_receives_resolved_exact_scope_and_inactive_reads_are_audited():
    service,factory=make_service();advance(service)
    service.list_visible_assessments(Actor("SYN-EMP-001"),as_of=date(2027,2,20),request_id="employee-scope",correlation_id="employee-scope")
    scope=factory.store.last_scope
    assert scope.own_assessment_ids==("SYN-ASM-001",) and scope.team_ids==() and not scope.diagnostic
    service.list_visible_assessments(Actor("SYN-ADM-001"),as_of=date(2027,2,20),request_id="admin-scope",correlation_id="admin-scope")
    assert factory.store.last_scope.configuration_versions==("SYN-CFG-001",)
    factory.store.users["SYN-EMP-001"].active=False
    result=service.list_visible_assessments(Actor("SYN-EMP-001"),as_of=date(2027,2,20),request_id="inactive-read",correlation_id="inactive-read")
    assert result.outcome=="Rejected" and any(a.request_id=="inactive-read" and a.outcome=="Denied" for a in factory.store.audits)


def test_platform_admin_remains_read_only_even_with_malformed_mutation_scope():
    service,factory=make_service();advance(service)
    factory.store.roles.append(RoleScopeRecord("malformed","SYN-PLAT-001","squad_admin",datetime(2027,1,1,tzinfo=UTC),configuration_scope="SYN-CFG-001"))
    result=service.schedule_assignment(Actor("SYN-PLAT-001"),request_id="platform-mutate",correlation_id="platform-mutate")
    assert result.code is RejectionCode.FORBIDDEN
