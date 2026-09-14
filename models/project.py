"""Project class. Owner: TEAMMATE 3."""


VALID_DIFFICULTIES = {"easy", "medium", "hard", "legendary"}


class Project:
    """A project owned by a user. Holds tasks."""

    _id_counter = 0

    def __init__(self, title, description, due_date, owner_id,
                 difficulty="medium", project_id=None):
        Project._id_counter += 1
        self._id = project_id if project_id is not None else Project._id_counter
        self._title = title
        self._description = description
        self._due_date = due_date
        self._owner_id = owner_id
        if difficulty not in VALID_DIFFICULTIES:
            raise ValueError(f"Invalid difficulty: {difficulty}")
        self._difficulty = difficulty
        self._task_ids = []

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        if not value or not value.strip():
            raise ValueError("Due date cannot be empty.")
        self._due_date = value.strip()

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        if value not in VALID_DIFFICULTIES:
            raise ValueError(f"Invalid difficulty: {value}")
        self._difficulty = value

    @property
    def task_ids(self) -> list:
        return self._task_ids.copy()

    def add_task(self, tid: int):
        if not isinstance(tid, int):
            raise TypeError("Task ID must be an integer.")
        if tid in self._task_ids:
            return False
        self._task_ids.append(tid)
        return True

    def remove_task(self, tid: int):
        """Remove a task from the project."""
        if tid in self._task_ids:
            self._task_ids.remove(tid)
            return True
        return False

    def has_task(self, tid: int) -> bool:
        """Check whether a task belongs to this project."""
        return tid in self._task_ids

    def task_count(self) -> int:
        """Return the number of tasks in the project."""
        return len(self._task_ids)

    def clear_tasks(self):
        """Remove all tasks from the project."""
        self._task_ids.clear()

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "owner_id": self._owner_id,
            "difficulty": self._difficulty,
            "task_ids": self._task_ids.copy(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Project":
        if not isinstance(d, dict):
            raise TypeError("Project data must be a dictionary.")

        required_fields = ["id", "title", "owner_id"]
        for field in required_fields:
            if field not in d:
                raise ValueError(f"Missing project field: {field}")

        project = cls.__new__(cls)
        project._id = d["id"]
        project._title = d["title"]
        project._description = d.get("description", "")
        project._due_date = d.get("due_date", "")
        project._owner_id = d["owner_id"]
        project._difficulty = d.get("difficulty", "medium")
        project._task_ids = list(d.get("task_ids", []))

        if project._id > cls._id_counter:
            cls._id_counter = project._id

        return project

    def __str__(self):
        return f"Project #{self._id} [{self._difficulty}]: {self._title}"

    def __repr__(self):
        return (
            f"Project(id={self._id}, "
            f"title='{self._title}', "
            f"owner_id={self._owner_id})"
        )

