"""In-memory event bus for local App Studio."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, DefaultDict, List
import uuid


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Event:
    id: str
    topic: str
    payload: dict
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {"id": self.id, "topic": self.topic, "payload": dict(self.payload), "created_at": self.created_at}


class EventBus:
    def __init__(self):
        self._subscribers: DefaultDict[str, List[Callable[[Event], None]]] = defaultdict(list)
        self._events: List[Event] = []

    def subscribe(self, topic: str, handler: Callable[[Event], None]) -> None:
        self._subscribers[topic].append(handler)

    def publish(self, topic: str, payload: dict) -> Event:
        event = Event(id=str(uuid.uuid4()), topic=topic, payload=payload)
        self._events.append(event)
        for handler in list(self._subscribers.get(topic, [])):
            handler(event)
        return event

    def recent(self, limit: int = 50) -> list[Event]:
        return self._events[-limit:]
