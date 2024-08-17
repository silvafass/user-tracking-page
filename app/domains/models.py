from uuid import UUID

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    uid: UUID
    first_name: str
    last_name: str
    username: str
    avatar: str
    email: str
    phone_number: str
    employment_title: str
    employment_key_skill: str
