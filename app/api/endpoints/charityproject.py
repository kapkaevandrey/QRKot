import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charityproject import (
    ProjectCreate, ProjectUpdate, ProjectRead,
)
from app.api.validators import (
    check_unique_attribute, check_can_delete_project, check_is_active,
    try_get_object_by_attribute, check_can_update_full_amount
)
from app.crud.charityproject import project_crud

router = APIRouter()


@router.get('/', response_model=list[ProjectRead])
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return await project_crud.get_multi(session)


@router.delete(
    '/{project_id}',
    response_model=ProjectRead,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> ProjectRead:
    project = await try_get_object_by_attribute(project_crud, 'id', project_id, session)
    await check_can_delete_project(project)
    await project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=ProjectRead,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
        project_id: int,
        data: ProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> ProjectRead:
    project = await try_get_object_by_attribute(project_crud, 'id', project_id, session)
    await check_is_active(project)
    if data.name is not None:
        await check_unique_attribute(project_crud, 'name', data.name, session)
    if data.full_amount is not None:
        await check_can_update_full_amount(project, data.full_amount)
        if project.invested_amount == data.full_amount:
            project.deactivate()
    project = await project_crud.update(project, data, session)
    return project


###################### In Work
@router.post(
    '/',
    response_model=ProjectRead,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
        data: ProjectCreate,
        session: AsyncSession = Depends(get_async_session)
) -> int:
    await check_unique_attribute(
        project_crud,
        'name', data.name, session,
    )
    project = await project_crud.create(data=data, session=session)
    # TODO логика инвестирования
    return project