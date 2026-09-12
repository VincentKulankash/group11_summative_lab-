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
    def id(self) -> str: 
        return self._id

    @property
    def name(self) -> str: 
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError('Name cannot be empty')

        self._name = value.strip()


    @property
    def email(self) -> str: 
        return self._email

    @email.setter
    def email(self, value: str):
        if '@' not in value or '.' not in value:
            raise ValueError('Invalid email address')

        self._email = value.strip().lower()

    @abstractmethod
    def role(self) -> str:
        """Return 'admin' or 'user'"""
        pass

    def __str__(self):
        return f"[{self.role()}] {self.name} <{self.email}>"

#this is complete 
