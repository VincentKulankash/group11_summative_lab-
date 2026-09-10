"""User class — inherits from Person. Owner: TEAMMATE 2."""
from models.person import Person
from utils.auth import hash_password, verify_password


class User(Person):
    """A registered user of TaskFlow."""

    def __init__(self, name, email, password, role="user", user_id=None):
        #TO DO (team member): call super().__init__, hash password, set role,
        #initialize self._project_ids = []


        super().__init__(name, email)
        if user_id is not None:
            self._id = user_id
        self._password_hash = hash_password(password)
        self._role = role
        self._project_ids = []

    def role(self) -> str:

        # TO DO (team member): return self._role
        return self._role

    def check_password(self, raw: str) -> bool:
        # TO DO (team member): return verify_password(raw, self._password_hash)

        return verify_password(raw, self._password_hash)

    def add_project(self, pid: int):
        # TO DO (team member): append pid to self._project_ids
        self._project_ids.append(pid)

    @property
    def project_ids(self) -> list:
        # TO DO (team member): return a copy of the list
        return list(self._project_ids)

    def to_dict(self) -> dict:
        # TO DO (team member)
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "password_hash": self._password_hash,
            "role": self._role,
            "project_ids": self._project_ids,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "User":
        # TO DO (team member): rebuild User from dict WITHOUT re-hashing password
        u = cls.__new__(cls)
        u._id = d["id"]
        u._name = d["name"]
        u._email = d["email"]
        u._password_hash = d["password_hash"]
        u._role = d.get("role", "user")
        u._project_ids = d.get("project_ids", [])
        return u