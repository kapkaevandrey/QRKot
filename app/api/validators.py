from http import HTTPStatus
from typing import Any

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD, ModelType
from app.models.charity_project import CharityProject


# подумать насчёт декорирования функции
async def check_unique_attribute(
        crud_obj: BaseCRUD,
        attr_name: str,
        attr_value: Any,
        session: AsyncSession
) -> None:
    result = await crud_obj.get_by_attribute(attr_name, attr_value, session)
    if result is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Field {attr_name} must be unique'
        )


async def try_get_object_by_attribute(
        crud_obj: BaseCRUD,
        attr_name: str,
        attr_value: Any,
        session: AsyncSession
) -> ModelType:
    result = await crud_obj.get_by_attribute(attr_name, attr_value, session)
    if result is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=(
                f'{crud_obj.model.__name__} '
                f'with {attr_name}={attr_value} is not found!'
            )
        )
    return result


async def check_is_active(
        obj: ModelType
):
    if not obj.is_active:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f'This {obj} is closed'
        )


async def check_can_delete_project(
        project: CharityProject
) -> None:
    await check_is_active(project)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='This project has already received funding'
        )


async def check_can_update_full_amount(
        project: CharityProject,
        new_full_amount: int
) -> None:
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f'Yoo cannot reduce the amount of the project '
                f'below the already invested funds in the amount of '
                f'{project.invested_amount}'
            )
        )
