from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import investment_process
from app.api.validators import (
    check_unique_attribute, check_can_delete_project, check_is_active,
    try_get_object_by_attribute, check_can_update_project,
)
from app.crud import project_crud
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    ProjectCreate, ProjectUpdate, ProjectRead,
)


router = APIRouter()


@router.get('/', response_model=List[ProjectRead])
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """
    ___You can see all cat projects.___
    """
    return await project_crud.get_multi(session)


@router.delete(
    '/{project_id}',
    response_model=ProjectRead,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """
    ___You can delete project if you have a superpower.___
    """
    project = await try_get_object_by_attribute(
        project_crud, 'id', project_id, session,
    )
    await check_can_delete_project(project)
    await project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=ProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
        project_id: int,
        data: ProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    ___You can update project if you have a superpower.___
    """
    project = await try_get_object_by_attribute(
        project_crud, 'id', project_id, session,
    )
    await check_is_active(project)
    await check_unique_attribute(project_crud, 'name', data.name, session)
    await check_can_update_project(project, data.full_amount)
    if data.full_amount and project.invested_amount == data.full_amount:
        await project.deactivate()
    return await project_crud.update(project, data, session)


@router.post(
    '/',
    response_model=ProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
        data: ProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    ___You can create project if you have a superpower.___
    - **name**: Name of the cat project
    - **full_amount**: How many money needs this project needs
    - **description**: Project descriptions
    """
    await check_unique_attribute(
        project_crud,
        'name', data.name, session,
    )
    project = await project_crud.create(data=data, session=session)
    project_id = project.id
    await investment_process(session)
    return await project_crud.get(project_id, session)
