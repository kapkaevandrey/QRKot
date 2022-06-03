from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import donation_crud
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.utils.investment import investment_process
from app.schemas.donation import (
    DonationCreate, DonationFullRead, DonationRead,
)
from app.schemas.user import UserRead


router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationFullRead],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """
    ___You can see all donations if you have a superpower.___
    """
    return await donation_crud.get_multi(session)


@router.get(
    '/my/',
    response_model=List[DonationRead],
    response_model_exclude_unset=True,
    dependencies=[Depends(current_user)]
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: UserRead = Depends(current_user),
):
    """
    ___You can see all you donation.___
    """
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
        user: UserRead = Depends(current_user),
):
    """
    ___You can make a donation.___
    - **full_amount**: How much money you can donate for our cats
    - **comment**: say something (optional)
    """
    donation = await donation_crud.create(data, session, user_id=user.id)
    donation_id = donation.id
    await investment_process(session, donation)
    return jsonable_encoder(await donation_crud.get(donation_id, session))
