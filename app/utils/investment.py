from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import donation_crud, project_crud
from app.models import CharityProject, Donation


async def investment_process(
        session: AsyncSession,
        invest_object=Union[CharityProject, Donation]
):
    request = dict(
        attr_name='fully_invested', attr_value=False,
        order_by='create_date', many=True,
    )
    if isinstance(invest_object, Donation):
        iter_crud = project_crud
    elif isinstance(invest_object, CharityProject):
        iter_crud = donation_crud
    else:
        raise TypeError(
            'Переданный объект не является'
            'экземпляром класса CharityProject или Donation'
        )
    iter_objects = await iter_crud.get_by_attribute(
        session=session, **request,
    )
    for obj in iter_objects:
        remain = obj.remain - invest_object.remain
        if remain == 0:
            obj.deactivate()
            invest_object.deactivate()
        elif remain > 0:
            obj.invested_amount += invest_object.remain
            invest_object.deactivate()
        else:
            invest_object.invested_amount += obj.remain
            obj.deactivate()
        if remain >= 0:
            break
    commit_objects = (invest_object, *iter_objects)
    session.add_all(commit_objects)
    await session.commit()
    [await session.refresh(obj) for obj in commit_objects]
