from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_project_admin, require_project_member
from app.models.user import User
from app.models.project import Project, ProjectMembership, ProjectRole
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectBase, ProjectDetail, ProjectMember

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=List[ProjectBase])
def list_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = (
        db.query(Project)
        .join(ProjectMembership)
        .filter(ProjectMembership.user_id == current_user.id, Project.is_archived == False)
        .all()
    )
    return projects


@router.post("", response_model=ProjectBase)
def create_project(payload: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = Project(
        name=payload.name,
        description=payload.description,
        owner_id=current_user.id,
    )
    db.add(project)
    db.flush()
    membership = ProjectMembership(
        project_id=project.id,
        user_id=current_user.id,
        role=ProjectRole.admin,
    )
    db.add(membership)
    db.commit()
    db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectDetail)
def get_project(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = require_project_member(project_id, current_user, db)
    memberships = (
        db.query(ProjectMembership, User)
        .join(User, ProjectMembership.user_id == User.id)
        .filter(ProjectMembership.project_id == project.id)
        .all()
    )
    members = [
        ProjectMember(
            user_id=u.id,
            email=u.email,
            full_name=u.full_name,
            role=m.role,
        )
        for m, u in memberships
    ]
    return ProjectDetail(
        id=project.id,
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
        is_archived=project.is_archived,
        created_at=project.created_at,
        updated_at=project.updated_at,
        members=members,
    )


@router.patch("/{project_id}", response_model=ProjectBase)
def update_project(project_id: int, payload: ProjectUpdate, project: Project = Depends(require_project_admin), db: Session = Depends(get_db)):
    if payload.name is not None:
        project.name = payload.name
    if payload.description is not None:
        project.description = payload.description
    if payload.is_archived is not None:
        project.is_archived = payload.is_archived
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.post("/{project_id}/members", response_model=ProjectMember)
def add_member(
    project_id: int,
    user_id: int,
    role: ProjectRole = ProjectRole.member,
    project: Project = Depends(require_project_admin),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    existing = (
        db.query(ProjectMembership)
        .filter(ProjectMembership.project_id == project.id, ProjectMembership.user_id == user.id)
        .first()
    )
    if existing:
        existing.role = role
        db.add(existing)
        db.commit()
        db.refresh(existing)
        membership = existing
    else:
        membership = ProjectMembership(
            project_id=project.id,
            user_id=user.id,
            role=role,
        )
        db.add(membership)
        db.commit()
        db.refresh(membership)
    return ProjectMember(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=membership.role,
    )


@router.delete("/{project_id}/members/{user_id}")
def remove_member(
    project_id: int,
    user_id: int,
    project: Project = Depends(require_project_admin),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    membership = (
        db.query(ProjectMembership)
        .filter(ProjectMembership.project_id == project.id, ProjectMembership.user_id == user_id)
        .first()
    )
    if membership is None:
        raise HTTPException(status_code=404, detail="Membership not found")
    if membership.user_id == project.owner_id:
        raise HTTPException(status_code=400, detail="Cannot remove project owner")
    db.delete(membership)
    db.commit()
    return {"detail": "removed"}
