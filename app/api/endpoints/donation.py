from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import DonationRead, DonationCreate
from app.schemas.user import UserRead
from app.api.utils import investment_process
router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationRead],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
) -> list[DonationRead]:
    return await donation_crud.get_multi(session)


@router.get(
    '/my/',
    response_model=list[DonationRead],
    response_model_exclude={'close_data', 'user_id', 'invested_amount', 'fully_invested'},
    dependencies=[Depends(current_user)]
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: UserRead = Depends(current_user),
) -> list[UserRead]:
    return await donation_crud.get_by_attribute(
        attr_name='user_id', attr_value=user.id, session=session, many=True
    )


@router.post(
    '/',
    response_model=DonationRead,
    response_model_exclude={'close_data', 'user_id', 'invested_amount', 'fully_invested'},
    dependencies=[Depends(current_user)]
)
async def create_donation(
        data: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: UserRead = Depends(current_user),
) -> DonationRead:
    donate = await donation_crud.create(data, session, user_id=user.id)
    await investment_process(session)
    return donate