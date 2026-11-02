"""Unit tests for content-minimized prototype adapters."""

from datetime import UTC, date, datetime

from app.documents import synthetic_artifact_hash
from app.notifications import MinimalNotification, NonDeliveringNotificationAdapter


def test_synthetic_artifact_hash_is_order_independent() -> None:
    first = synthetic_artifact_hash({"version": "SYN-ASMV-002", "kind": "summary"})
    second = synthetic_artifact_hash({"kind": "summary", "version": "SYN-ASMV-002"})

    assert first == second
    assert len(first) == 64


def test_non_delivering_adapter_returns_only_safe_observation() -> None:
    notification = MinimalNotification(
        event_id="SYN-NOTIF-001",
        recipient_id="SYN-EMP-001",
        template_version="prototype-v1",
        record_id="SYN-ASM-001",
        trigger="due",
        occurrence_id="SYN-OCC-001",
        status="Assigned",
        due_date=date(2027, 2, 15),
    )

    observation = NonDeliveringNotificationAdapter().deliver(
        notification,
        adapter_request_id="SYN-ATTEMPT-001",
        attempted_at=datetime(2027, 2, 15, tzinfo=UTC),
    )

    assert observation.outcome == "not_delivered_prototype"
    assert observation.manual_retry_allowed is True
    assert observation.production_retry_policy is None
    assert not hasattr(notification, "assessment_result")
    assert not hasattr(notification, "narrative")
