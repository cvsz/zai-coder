from zai_coder.core.approvals import ActionApprover

def test_action_approver():
    approver = ActionApprover(apply_mode=False)
    assert approver.check("run_command", "ls") is False
    assert approver.check("unknown_action", "details") is False
    
    approver2 = ActionApprover(apply_mode=True)
    
    # Needs user approval, but since we mock or test unattended, we can just test requires_approval
    assert approver2.requires_approval("run_command") is True
    assert approver2.requires_approval("write_file") is True
    assert approver2.requires_approval("delete_file") is True
    assert approver2.requires_approval("safe_read") is False
    
    assert approver2.check("safe_read", "file.txt") is True
