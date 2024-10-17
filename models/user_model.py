from dataclasses import dataclass



"""
class UserModel:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
        )
"""

@dataclass
class User:
    name:str=None
    age:int=None
    email:str=None


