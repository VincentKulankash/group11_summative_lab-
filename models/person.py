from abc import ABC, abstractmethod

class Person(ABC):
    _id_counter = 0

    def __init__(self, name:str, email: str):
        # To do (Vincent Kulankash) validate + store _name, _email, assign _id 

        Person._id_counter += 1 
        self._id = Person._id_counter
        self.name = name
        self.email = email

    @property
    def id(self): return self._id

    @property
    def name(self): return self._name

    @property
    def email(self): return self._email

    @abstractmethod
    def role(self) -> str:
        """Return 'admin' or 'user'"""
        pass

    def __str__(self):
        return f"[{self.role()}] {self.name} <{self.email}>"

    