"""Structured event bus."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

from .models import StructuredEvent


Subscriber = Callable[[StructuredEvent], None]


class StructuredEventBus:
    def __init__(self):
        self._events: list[StructuredEvent] = []
        self._subscribers: dict[str, list[Subscriber]] = defaultdict(list)

    def publish(self, event: StructuredEvent) -> StructuredEvent:
        issues = event.validate()
        if issues:
            raise ValueError("; ".join(issues))
        self._events.append(event)
        for subscriber in self._subscribers.get(event.topic, []):
            subscriber(event)
        for subscriber in self._subscribers.get("*", []):
            subscriber(event)
        return event

    def subscribe(self, topic: str, subscriber: Subscriber) -> None:
        if not topic:
            raise ValueError("topic required")
        self._subscribers[topic].append(subscriber)

    def list_events(self, limit: int = 100, level: str | None = None) -> list[dict]:
        events = self._events[-limit:]
        if level:
            events = [event for event in events if event.level == level]
        return [event.to_dict() for event in events]


def default_event_bus() -> StructuredEventBus:
    bus = StructuredEventBus()
    bus.publish(StructuredEvent("system.start", "info", "observability suite initialized"))
    return bus
