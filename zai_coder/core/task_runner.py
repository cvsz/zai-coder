from typing import Optional
from .task_store import TaskStore
from .approvals import ActionApprover
from .tasks import Task

class TaskRunner:
    def __init__(self, store: TaskStore, approver: ActionApprover):
        self.store = store
        self.approver = approver

    def run(self, task_id: int):
        task_data = self.store.get_task(task_id)
        if not task_data:
            print(f"Task {task_id} not found.")
            return

        if task_data["state"] in ["completed", "failed", "cancelled"]:
            print(f"Task {task_id} already finished.")
            return

        print(f"Starting task {task_id}: {task_data['title']}")
        self.store.update_task_state(task_id, "running")
        self.store.add_event(task_id, "start", "Task execution started.")

        try:
            # Check approval
            if not self.approver.approve("run_command", f"Execute task '{task_data['title']}'"):
                self.store.update_task_state(task_id, "cancelled")
                self.store.add_event(task_id, "cancel", "Task cancelled by user.")
                print(f"Task {task_id} cancelled.")
                return

            self.store.update_task_state(task_id, "completed")
            self.store.add_event(task_id, "complete", "Task finished successfully.")
            self.store.add_output(task_id, "assistant", "Done.")
            print(f"Task {task_id} completed successfully.")

        except Exception as e:
            self.store.update_task_state(task_id, "failed", error=str(e))
            self.store.add_event(task_id, "fail", f"Task failed: {e}")
            print(f"Task {task_id} failed: {e}")
