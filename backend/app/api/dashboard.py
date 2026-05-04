from typing import Dict, List
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskOut

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/my-tasks", response_model=Dict[TaskStatus, List[TaskOut]])
def my_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.assignee_id == current_user.id).all()
    result: Dict[TaskStatus, List[TaskOut]] = {s: [] for s in TaskStatus}
    for t in tasks:
        result[t.status].append(t)
    return result


@router.get("/overdue", response_model=List[TaskOut])
def overdue(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    tasks = (
        db.query(Task)
        .filter(Task.assignee_id == current_user.id)
        .filter(Task.due_date != None)
        .filter(Task.due_date < now)
        .filter(Task.status != TaskStatus.done)
        .all()
    )
    return tasks
