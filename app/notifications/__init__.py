"""Minimal-content notification contracts and non-delivering prototype adapter."""

from app.notifications.prototype import (
    DeliveryObservation,
    MinimalNotification,
    NonDeliveringNotificationAdapter,
)

__all__ = [
    "DeliveryObservation",
    "MinimalNotification",
    "NonDeliveringNotificationAdapter",
]
