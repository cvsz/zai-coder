from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class Task:
    id: int
    title: str
    agent: str
    prompt: str
    state: str
    created_at: float
    updated_at: float
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    error: Optional[str] = None

@dataclass
class TaskEvent:
    id: int
    task_id: int
    event_type: str
    message: str
    created_at: float

@dataclass
class TaskOutput:
    id: int
    task_id: int
    role: str
    content: str
    created_at: float
