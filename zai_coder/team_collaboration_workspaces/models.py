from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class TeamWorkspace:
    id: str
    org_id: str
    name: str
    visibility: str = "private"
    status: str = "active"
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.org_id or not self.name: issues.append("workspace id, org_id, and name required")
        if self.visibility not in {"private","org","public"}: issues.append("invalid workspace visibility")
        if self.status not in {"active","archived","suspended"}: issues.append("invalid workspace status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class TeamMember:
    id: str
    workspace_id: str
    user_ref: str
    role: str = "viewer"
    status: str = "active"
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.workspace_id or not self.user_ref: issues.append("member id, workspace_id, and user_ref required")
        if self.role not in {"owner","admin","operator","reviewer","viewer","auditor"}: issues.append("invalid member role")
        if self.status not in {"active","invited","suspended","removed"}: issues.append("invalid member status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class ReviewQueueItem:
    id: str
    workspace_id: str
    title: str
    item_type: str = "change"
    status: str = "open"
    priority: str = "normal"
    requested_by: str = "system"
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.workspace_id or not self.title: issues.append("review item id, workspace_id, and title required")
        if self.item_type not in {"change","release","content","policy","access","incident"}: issues.append("invalid review item_type")
        if self.status not in {"open","in_review","approved","rejected","closed"}: issues.append("invalid review status")
        if self.priority not in {"low","normal","high","urgent"}: issues.append("invalid review priority")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class WorkspaceInvitation:
    id: str
    workspace_id: str
    invitee_ref: str
    role: str = "viewer"
    status: str = "draft"
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.workspace_id or not self.invitee_ref: issues.append("invitation id, workspace_id, and invitee_ref required")
        if self.role not in {"admin","operator","reviewer","viewer","auditor"}: issues.append("invalid invitation role")
        if self.status not in {"draft","review","approved","cancelled"}: issues.append("invalid invitation status")
        if not self.dry_run: issues.append("workspace invitations must be dry-run by default")
        return issues
    def to_dict(self): return self.__dict__.copy()
