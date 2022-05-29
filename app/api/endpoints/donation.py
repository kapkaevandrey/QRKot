from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.schemas.donation import DonationRead, DonationCreate, DonationReadFull
from app.schemas.user import UserRead

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationReadFull],
    dependencies=[Depends(current_superuser)]
)
def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
) -> int:
    return 123


@router.post(
    '/',
    response_model=DonationRead,
    dependencies=[Depends(current_user)]
)
def create_donation(
        data: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: UserRead = Depends(current_user),
) -> int:
    return 123


@router.get(
    '/my/',
    response_model=list[DonationRead],
    dependencies=[Depends(current_user)]
)
def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: UserRead = Depends(current_user),
) -> int:
    return 123
