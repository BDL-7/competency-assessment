"""Safe notification values for the synthetic, non-delivering prototype."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class MinimalNotification:
    """A deliberately narrow payload that cannot carry assessment narrative."""

    event_id: str
    recipient_id: str
    template_version: str
    record_id: str
    trigger: str
    occurrence_id: str
    status: str
    due_date: date | None = None


@dataclass(frozen=True)
class DeliveryObservation:
    event_id: str
    adapter_request_id: str
    attempted_at: datetime
    outcome: str
    manual_retry_allowed: bool
    production_retry_policy: str | None = None
    safe_failure_category: str | None = None


class NonDeliveringNotificationAdapter:
    """Record an attributable test outcome without sending a message."""

    def deliver(
        self,
        notification: MinimalNotification,
        *,
        adapter_request_id: str,
        attempted_at: datetime,
    ) -> DeliveryObservation:
        return DeliveryObservation(
            event_id=notification.event_id,
            adapter_request_id=adapter_request_id,
            attempted_at=attempted_at,
            outcome="not_delivered_prototype",
            manual_retry_allowed=True,
            production_retry_policy=None,
        )
