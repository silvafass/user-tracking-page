from typing import Literal
from uuid import UUID

from pydantic import BaseModel
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


class TrackingBase(SQLModel):
    description: str


class Tracking(TrackingBase, table=True):
    id: str = Field(primary_key=True)
    metric_type: str = Field(primary_key=True, regex="page_access|visibility")


class TrackingPublic(TrackingBase):
    id: str
    metric_type: Literal["page_access", "visibility"]


class TrackingReportPublic(BaseModel):
    metric_type: Literal["page_access", "visibility"]
    description: str
    total: str


class ListTrackingReportPublic(BaseModel):
    data: list[TrackingReportPublic] | None = None
    count: int
