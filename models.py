from sqlalchemy import table
from sqlmodel import SQLModel, Field
from typing import Optional


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None,  primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None



class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str