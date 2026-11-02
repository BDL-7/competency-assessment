"""Approved S0-04A configure-through-renewal scenario over service ports."""
from datetime import UTC,datetime
from app.domain import AssessmentState,NotificationTrigger
from app.services import Actor,ServiceActor
from tests.integration.test_workflow_service import advance,make_service

def test_complete_synthetic_path_has_all_seven_logical_triggers():
    service,factory=make_service();advance(service);svc=ServiceActor("SYN-SVC-001")
    occurrences=((NotificationTrigger.UPCOMING_DUE,datetime(2027,2,10,tzinfo=UTC)),
                 (NotificationTrigger.DUE,datetime(2027,2,15,tzinfo=UTC)),
                 (NotificationTrigger.OVERDUE,datetime(2027,2,16,tzinfo=UTC)))
    for offset,(trigger,when) in enumerate(occurrences):
        service.create_scheduled_notification(svc,assessment_id="SYN-ASM-001",trigger=trigger,
            occurrence=when,request_id=f"e2e-event-{offset}",correlation_id="e2e-events")
    service.sign_testing_personnel(Actor("SYN-EMP-001"),assessment_id="SYN-ASM-001",
        version_id="SYN-ASMV-002",request_id="e2e-sign",correlation_id="e2e-sign",expected_version=5)
    result=service.finalize(Actor("SYN-TS-001"),assessment_id="SYN-ASM-001",
        version_id="SYN-ASMV-002",request_id="e2e-final",correlation_id="e2e-final",expected_version=6)
    assert result.state==AssessmentState.FINALIZED.value
    assert {event.trigger for event in factory.store.events.values()}=={item.value for item in NotificationTrigger}
