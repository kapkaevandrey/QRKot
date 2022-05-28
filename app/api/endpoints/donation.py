from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session


router = APIRouter()


@router.get('/')
def get_donation(
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return 123


@router.post('/')
def get_donation(
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return 123


@router.get('/my/')
def get_donation(
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return 123
