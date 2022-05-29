from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charityproject import (
    ProjectCreate, ProjectUpdate, ProjectRead,
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[ProjectRead]
)
def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return 0


@router.post(
    '/',
    response_model=ProjectRead,
    dependencies=[Depends(current_superuser)]
)
def create_project(
        data: ProjectCreate,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return 0


@router.delete(
    '/{project_id}',
    response_model=ProjectRead,
    dependencies=[Depends(current_superuser)]
)
def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return project_id


@router.patch(
    '/{project_id}',
    response_model=ProjectRead,
    dependencies=[Depends(current_superuser)]
)
def update_project(
        project_id: int,
        data: ProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return project_id
