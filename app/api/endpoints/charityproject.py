from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session

router = APIRouter()


@router.get('/')
def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return 0


@router.post('/')
def create_project(
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return 0


@router.delete('/{project_id}')
def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return project_id


@router.patch('/{project_id}')
def update_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return project_id
