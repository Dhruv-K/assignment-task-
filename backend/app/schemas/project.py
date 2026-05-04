from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional, List

from app.models.project import ProjectRole


class ProjectCreate(BaseModel):
    name: constr(min_length=1)
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[constr(min_length=1)] = None
    description: Optional[str] = None
    is_archived: Optional[bool] = None


class ProjectMember(BaseModel):
    user_id: int
    email: str
    full_name: str
    role: ProjectRole


class ProjectBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectDetail(ProjectBase):
    members: List[ProjectMember] = []
