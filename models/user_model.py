from typing import Dict
from pydantic import BaseModel # type: ignore

# authenticating user's class model
class UserModel(BaseModel): # type: ignore
    email: str
    password: str
    
    def to_json(self) -> Dict[str, str]:
        return {
            'email': self.email,
            'password': self.password
        }
    @classmethod
    def from_json(cls, data: Dict[str, str]) -> 'UserModel':
        return cls(**data)
   