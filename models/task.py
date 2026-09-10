"""Task class. Owner: TEAMMATE 4."""


class Task:
    """A task belonging to a project."""

    _id_counter = 0
    VALID_STATUSES = {"todo", "in-progress", "done"}

    def __init__(self, title, project_id, assigned_to=None, status="todo", task_id=None):
        # TO DO (team member): assign id, store fields, validate status
        Task._id_counter += 1
        self._id = task_id if task_id is not None else Task._id_counter
        self._title = title
        self._project_id = project_id
        self._assigned_to = assigned_to
        if status not in Task.VALID_STATUSES:
            raise ValueError(f"Bad status: {status}")
        self._status = status

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def status(self):
        return self._status

    @property
    def project_id(self):
        return self._project_id

    @property
    def assigned_to(self):
        return self._assigned_to

    @status.setter
    def status(self, value):
        # TO DO (team member): raise ValueError if value not in VALID_STATUSES
        if value not in Task.VALID_STATUSES:
            raise ValueError(f"Bad status: {value}")
        self._status = value

    def complete(self):
        # TO DO (team member): set status to "done"
        self._status = "done"

    def to_dict(self) -> dict:
        # TO DO (team member)
        return {
            "id": self._id,
            "title": self._title,
            "status": self._status,
            "project_id": self._project_id,
            "assigned_to": self._assigned_to,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        # TO DO (team member)
        t = cls.__new__(cls)
        t._id = d["id"]
        t._title = d["title"]
        t._status = d["status"]
        t._project_id = d["project_id"]
        t._assigned_to = d.get("assigned_to")
        return t

    def __str__(self):
        return f"Task #{self._id} [{self._status}] {self._title}"