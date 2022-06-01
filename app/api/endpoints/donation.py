from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import DonationFullRead, DonationCreate, DonationRead
from app.schemas.user import UserDB
router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationFullRead],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
) -> list[DonationFullRead]:
    return await donation_crud.get_multi(session)


@router.get(
    '/my/',
    response_model=list[DonationRead],
    response_model_exclude_unset=True,
    dependencies=[Depends(current_user)]
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user),
):
    donations = await donation_crud.get_by_attribute(
        attr_name='user_id', attr_value=user.id, session=session, many=True
    )
    return jsonable_encoder(donations)


@router.post(
    '/',
    response_model=DonationRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_donation(
        data: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user),
) -> DonationFullRead:
    donate = await donation_crud.create(data, session, user_id=user.id)
    # TODO await investment_process(session)
    return jsonable_encoder(donate)
