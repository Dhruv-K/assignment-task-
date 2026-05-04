from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional

from app.models.task import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: constr(min_length=1)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1)] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskOut(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    assignee_id: Optional[int]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
