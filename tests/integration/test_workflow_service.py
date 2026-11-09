"""Framework-neutral integration checks across workflow service ports."""
from datetime import UTC,date,datetime
from app.domain import AssessmentState,NotificationTrigger,RejectionCode
from app.services import Actor,DraftContent,ServiceActor,build_workflow_service
from tests.unit.fakes import FakeFactory

NOW=datetime(2027,2,20,15,30,tzinfo=UTC)
CONTENT=DraftContent("Synthetic context","Initial","SYN-PROCESS-01","Synthetic observation","Synthetic specimen","Synthetic testing and instrument context","Synthetic evidence","Recorded by assessor",has_gap=True)

def make_service(fault=None):
    factory=FakeFactory();return build_workflow_service(factory,clock=lambda:NOW,finalization_fault=fault),factory

def advance(service):
    admin=Actor("SYN-ADM-001");assessor=Actor("SYN-ASR-001")
    assert service.configure_synthetic_scenario(admin,request_id="r1",correlation_id="c1").outcome=="Succeeded"
    assert service.schedule_assignment(admin,request_id="r2",correlation_id="c2").state=="Scheduled"
    assert service.release_assignment(admin,request_id="r3",correlation_id="c3",expected_version=1).state=="Assigned"
    assert service.begin_assessment(assessor,assessment_id="SYN-ASM-001",request_id="r4",correlation_id="c4",expected_version=1).state=="In progress"
    service.save_draft(assessor,assessment_id="SYN-ASM-001",content=CONTENT,followup_description=None,request_id="r5",correlation_id="c5",expected_draft_version=1)
    returned=service.submit_assessment(assessor,assessment_id="SYN-ASM-001",request_id="r6",correlation_id="c6",expected_version=2)
    assert returned.code is RejectionCode.FOLLOWUP_REQUIRED and returned.reference_id=="SYN-ASMV-001"
    corrected=service.save_draft(assessor,assessment_id="SYN-ASM-001",content=CONTENT,followup_description="Synthetic follow-up documented",request_id="r7",correlation_id="c7",expected_draft_version=1)
    assert corrected.state==AssessmentState.IN_PROGRESS.value and corrected.version==4
    submitted=service.submit_assessment(assessor,assessment_id="SYN-ASM-001",request_id="r8",correlation_id="c8",expected_version=4)
    assert submitted.reference_id=="SYN-ASMV-002";return submitted

def test_two_versions_and_clock_owned_finalization():
    service,factory=make_service();advance(service)
    service.sign_testing_personnel(Actor("SYN-EMP-001"),assessment_id="SYN-ASM-001",version_id="SYN-ASMV-002",request_id="r9",correlation_id="c9",expected_version=5)
    result=service.finalize(Actor("SYN-TS-001"),assessment_id="SYN-ASM-001",version_id="SYN-ASMV-002",request_id="r10",correlation_id="c10",expected_version=6)
    assert result.state==AssessmentState.FINALIZED.value
    assert [v.number for v in factory.store.versions.values()]==[1,2]
    assert all(v.supersedes_id is None for v in factory.store.versions.values())
    assert factory.store.renewals[0].completion_date==NOW.date()
    assert factory.store.renewals[0].next_due_date==date(2028,2,20)
    assert len(factory.store.documents[0].sha256)==64

def test_replay_precedes_concurrency_and_known_rejection_is_stored():
    service,factory=make_service();advance(service);actor=Actor("SYN-ASR-001")
    replay=service.submit_assessment(actor,assessment_id="SYN-ASM-001",request_id="r8",correlation_id="new",expected_version=4)
    conflict=service.submit_assessment(actor,assessment_id="SYN-ASM-001",request_id="r8",correlation_id="new",expected_version=999)
    stale=service.submit_assessment(actor,assessment_id="SYN-ASM-001",request_id="stale",correlation_id="stale",expected_version=999)
    assert replay.replayed and conflict.code is RejectionCode.IDEMPOTENCY_CONFLICT
    assert stale.code is RejectionCode.STALE_VERSION and any(key[3]=="stale" for key in factory.store.idempotency)

def test_scheduled_trigger_validation_and_attempt_retries():
    service,factory=make_service();advance(service);svc=ServiceActor("SYN-SVC-001")
    bad=service.create_scheduled_notification(svc,assessment_id="SYN-ASM-001",trigger=NotificationTrigger.DUE,occurrence=datetime(2027,2,14,tzinfo=UTC),request_id="bad",correlation_id="bad")
    assert bad.code is RejectionCode.INVALID_STATE
    event=service.create_scheduled_notification(svc,assessment_id="SYN-ASM-001",trigger=NotificationTrigger.DUE,occurrence=datetime(2027,2,15,tzinfo=UTC),request_id="due",correlation_id="due")
    first=service.record_notification_attempt(svc,event_id=event.reference_id,adapter_request_id="attempt-1",correlation_id="a")
    replay=service.record_notification_attempt(svc,event_id=event.reference_id,adapter_request_id="attempt-1",correlation_id="b")
    second=service.record_notification_attempt(svc,event_id=event.reference_id,adapter_request_id="attempt-2",correlation_id="c")
    assert replay.replayed and len(factory.store.attempts)==2 and first.reference_id!=second.reference_id

def test_finalization_failure_rolls_back_and_same_request_retries():
    failures=[True]
    def fault():
        if failures and failures.pop():raise RuntimeError("injected")
    service,factory=make_service(fault);advance(service)
    service.sign_testing_personnel(Actor("SYN-EMP-001"),assessment_id="SYN-ASM-001",version_id="SYN-ASMV-002",request_id="r9",correlation_id="c9",expected_version=5)
    failed=service.finalize(Actor("SYN-TS-001"),assessment_id="SYN-ASM-001",version_id="SYN-ASMV-002",request_id="r10",correlation_id="c10",expected_version=6)
    assert failed.outcome=="Failed" and failed.code is RejectionCode.DEPENDENCY_UNAVAILABLE
    assert len(factory.store.signatures)==1 and not factory.store.documents and not factory.store.renewals
    retried=service.finalize(Actor("SYN-TS-001"),assessment_id="SYN-ASM-001",version_id="SYN-ASMV-002",request_id="r10",correlation_id="c10",expected_version=6)
    assert retried.outcome=="Succeeded" and len(factory.store.signatures)==2

def test_navigation_pointer_mismatch_fails_closed():
    service,factory=make_service();advance(service)
    assessment=factory.store.assessments["SYN-ASM-001"];assessment.state=AssessmentState.IN_PROGRESS.value
    factory.store.drafts[assessment.current_draft_id].assessment_id="SYN-OTHER-ASM"
    result=service.save_draft(Actor("SYN-ASR-001"),assessment_id=assessment.id,content=CONTENT,followup_description="Synthetic follow-up",request_id="pointer",correlation_id="pointer",expected_draft_version=2)
    assert result.outcome=="Failed" and result.code is RejectionCode.DEPENDENCY_UNAVAILABLE

def test_draft_rejects_inconsistent_element_without_competency_inference():
    service,_=make_service();admin=Actor("SYN-ADM-001");assessor=Actor("SYN-ASR-001")
    service.configure_synthetic_scenario(admin,request_id="x1",correlation_id="x1")
    service.schedule_assignment(admin,request_id="x2",correlation_id="x2")
    service.release_assignment(admin,request_id="x3",correlation_id="x3",expected_version=1)
    service.begin_assessment(assessor,assessment_id="SYN-ASM-001",request_id="x4",correlation_id="x4",expected_version=1)
    invalid=DraftContent("Synthetic","Initial","SYN-PROCESS-01","Observation","Specimen","Testing","Evidence","Recorded",element_result="successful",has_gap=True)
    result=service.save_draft(assessor,assessment_id="SYN-ASM-001",content=invalid,
        followup_description=None,request_id="x5",correlation_id="x5",expected_draft_version=1)
    assert result.code is RejectionCode.INVALID_INPUT

def test_nonfinalization_write_failure_is_safe_and_rolls_back():
    service,factory=make_service();admin=Actor("SYN-ADM-001")
    service.configure_synthetic_scenario(admin,request_id="w1",correlation_id="w1")
    factory.fail_on.add("add_assignment")
    result=service.schedule_assignment(admin,request_id="w2",correlation_id="write-failure")
    assert result.outcome=="Failed" and result.code is RejectionCode.DEPENDENCY_UNAVAILABLE
    assert not factory.store.assignments and not any(key[3]=="w2" for key in factory.store.idempotency)

def test_query_failure_is_minimized_and_rolls_back():
    service,factory=make_service();advance(service);factory.fail_on.add("query")
    before=len(factory.store.audits)
    result=service.list_visible_assessments(Actor("SYN-EMP-001"),as_of=date(2027,2,20),request_id="q-fail",correlation_id="query-failure")
    assert result.outcome=="Failed" and result.code=="DEPENDENCY_UNAVAILABLE" and result.items==()
    assert len(factory.store.audits)==before

def test_all_scheduled_triggers_reject_finalized_assessment():
    service,factory=make_service();advance(service)
    service.sign_testing_personnel(Actor("SYN-EMP-001"),assessment_id="SYN-ASM-001",version_id="SYN-ASMV-002",request_id="f-sign",correlation_id="f-sign",expected_version=5)
    service.finalize(Actor("SYN-TS-001"),assessment_id="SYN-ASM-001",version_id="SYN-ASMV-002",request_id="f-final",correlation_id="f-final",expected_version=6)
    svc=ServiceActor("SYN-SVC-001")
    cases=((NotificationTrigger.UPCOMING_DUE,datetime(2027,2,14,tzinfo=UTC)),(NotificationTrigger.DUE,datetime(2027,2,15,tzinfo=UTC)),(NotificationTrigger.OVERDUE,datetime(2027,2,16,tzinfo=UTC)))
    for index,(trigger,when) in enumerate(cases):
        result=service.create_scheduled_notification(svc,assessment_id="SYN-ASM-001",trigger=trigger,occurrence=when,request_id=f"final-event-{index}",correlation_id="final-events")
        assert result.code is RejectionCode.INVALID_STATE

def test_service_principal_is_distinct_and_platform_admin_cannot_emit_events():
    service,factory=make_service();advance(service)
    assert factory.store.users.get("SYN-SVC-001") is None
    assert factory.store.service_principals["SYN-SVC-001"].active
    before=len(factory.store.events)
    result=service.create_scheduled_notification(Actor("SYN-PLAT-001"),assessment_id="SYN-ASM-001",trigger=NotificationTrigger.DUE,occurrence=datetime(2027,2,15,tzinfo=UTC),request_id="platform-event",correlation_id="platform-event")
    assert result.code is RejectionCode.FORBIDDEN and len(factory.store.events)==before
