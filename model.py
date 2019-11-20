from pydantic import BaseModel, Schema
from typing import List


class UsersAddDataModel(BaseModel):
    id: int = Schema(..., title="Employee Id")
    name: str = Schema(..., title="Name of the employee", min_length=2)
    email: str = Schema(..., title="Email of the employee")


class UsersAddModel(BaseModel):
    userDetails: List[UsersAddDataModel] = None


class UsersUpdateModel(BaseModel):
    name: str = Schema(..., title="Name of the employee", min_length=2)
    email: str = Schema(..., title="Email of the employee")
