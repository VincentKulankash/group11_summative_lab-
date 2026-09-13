from enum import Enum


class TaskStatus(Enum):
    TODO = "Todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Task:
    def __init__(self, task_id, title, status=TaskStatus.TODO,
                 assigned_user=None, project=None):
        self.id = task_id
        self.title = title
        self.status = status
        self.assigned_user = assigned_user
        self.project = project

    def mark_complete(self):
        """Mark the task as completed."""
        self.status = TaskStatus.DONE

    def to_dict(self):
        """Convert the task to a dictionary for JSON saving."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "assigned_user": self.assigned_user,
            "project": self.project,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task from a dictionary."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            status=TaskStatus(data.get("status", TaskStatus.TODO.value)),
            assigned_user=data.get("assigned_user"),
            project=data.get("project"),
        )
