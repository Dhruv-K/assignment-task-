from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User
from app.models.project import Project, ProjectMembership, ProjectRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        sub: str | None = payload.get("sub")
        if sub is None:
            raise credentials_exception
        user_id = int(sub)
    except JWTError:
        raise credentials_exception
    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user


def get_project_and_membership(project_id: int, current_user: User, db: Session) -> tuple[Project, ProjectMembership]:
    project = db.get(Project, project_id)
    if project is None or project.is_archived:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    membership = (
        db.query(ProjectMembership)
        .filter(ProjectMembership.project_id == project.id, ProjectMembership.user_id == current_user.id)
        .first()
    )
    if membership is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project")
    return project, membership


def require_project_admin(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Project:
    project, membership = get_project_and_membership(project_id, current_user, db)
    if membership.role != ProjectRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return project


def require_project_member(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Project:
    project, membership = get_project_and_membership(project_id, current_user, db)
    return project
