"""Streaming event buffer foundation.

This is framework-neutral. Future HTTP/WebSocket servers can consume the events.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List
import uuid


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class StreamEvent:
    id: str
    run_id: str
    event_type: str
    data: dict
    created_at: str = field(default_factory=now_iso)

    def to_sse(self) -> str:
        return f"id: {self.id}\nevent: {self.event_type}\ndata: {self.data}\n\n"


class RunStream:
    def __init__(self):
        self.events: List[StreamEvent] = []

    def emit(self, run_id: str, event_type: str, data: dict) -> StreamEvent:
        event = StreamEvent(id=str(uuid.uuid4()), run_id=run_id, event_type=event_type, data=data)
        self.events.append(event)
        return event

    def for_run(self, run_id: str) -> list[StreamEvent]:
        return [event for event in self.events if event.run_id == run_id]
