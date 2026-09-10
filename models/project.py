"""Project class. Owner: TEAMMATE 3."""


class Project:
    """A project owned by a user. Holds tasks."""

    _id_counter = 0

    def __init__(self, title, description, due_date, owner_id, project_id=None):
        # TO DO (team member ): assign id, store fields, initialize self._task_ids = []
        Project._id_counter += 1
        self._id = project_id if project_id is not None else Project._id_counter
        self._title = title
        self._description = description
        self._due_date = due_date
        self._owner_id = owner_id
        self._task_ids = []

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def due_date(self):
        return self._due_date

    @property
    def task_ids(self) -> list:
        # TO DO (team member): return a copy
        return list(self._task_ids)

    def add_task(self, tid: int):
        # TO DO (team member)
        self._task_ids.append(tid)

    def to_dict(self) -> dict:
        # TO DO (team member)
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "owner_id": self._owner_id,
            "task_ids": self._task_ids,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Project":
        # TO DO (team member)
        p = cls.__new__(cls)
        p._id = d["id"]
        p._title = d["title"]
        p._description = d.get("description", "")
        p._due_date = d.get("due_date", "")
        p._owner_id = d["owner_id"]
        p._task_ids = d.get("task_ids", [])
        return p

    def __str__(self):
        return f"Project #{self._id}: {self._title}"