from __future__ import annotations

def approval_decision(apply: bool, approval_id: str = '') -> dict:
    if not apply:
        return {'allowed': True, 'reason': 'dry-run-does-not-require-approval'}
    if approval_id.startswith('approved_') and len(approval_id) >= 16:
        return {'allowed': True, 'reason': 'approval-present'}
    return {'allowed': False, 'reason': 'apply-requires-approval-id'}
