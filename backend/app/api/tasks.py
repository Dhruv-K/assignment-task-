from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_project_member, require_project_admin
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.models.project import Project
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/projects/{project_id}/tasks", response_model=List[TaskOut])
def list_tasks(
    project_id: int,
    status: Optional[TaskStatus] = Query(default=None),
    assignee_id: Optional[int] = Query(default=None),
    overdue: Optional[bool] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = require_project_member(project_id, current_user, db)
    q = db.query(Task).filter(Task.project_id == project.id)
    if status is not None:
        q = q.filter(Task.status == status)
    if assignee_id is not None:
        q = q.filter(Task.assignee_id == assignee_id)
    if overdue:
        now = datetime.utcnow()
        q = q.filter(Task.due_date != None, Task.due_date < now, Task.status != TaskStatus.done)
    tasks = q.order_by(Task.created_at.desc()).all()
    return tasks


@router.post("/projects/{project_id}/tasks", response_model=TaskOut)
def create_task(
    project_id: int,
    payload: TaskCreate,
    project: Project = Depends(require_project_admin),
    db: Session = Depends(get_db),
):
    task = Task(
        project_id=project.id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        assignee_id=payload.assignee_id,
        due_date=payload.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    require_project_member(task.project_id, current_user, db)
    return task


@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    require_project_member(task.project_id, current_user, db)
    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.status is not None:
        task.status = payload.status
    if payload.priority is not None:
        task.priority = payload.priority
    if payload.assignee_id is not None:
        task.assignee_id = payload.assignee_id
    if payload.due_date is not None:
        task.due_date = payload.due_date
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    require_project_admin(task.project_id, current_user, db)
    db.delete(task)
    db.commit()
    return {"detail": "deleted"}
