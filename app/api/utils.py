import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.donation import donation_crud
from app.crud.charityproject import project_crud


async def investment_process(session: AsyncSession) -> None:
    donations = await donation_crud.get_by_attribute(
        attr_name='fully_invested',
        attr_value=False,
        session=session,
        many=True, order_by='create_date'
    )
    if not donations:
        return
    projects = await project_crud.get_by_attribute(
        attr_name='fully_invested',
        attr_value=False,
        session=session,
        many=True, order_by='create_date'
    )
    current_donate = 0
    for project in projects:
        for donate in donations[current_donate:]:
            remain = project.remain - donate.remain
            if remain == 0:
                project.deactivate()
                donate.deactivate()
                current_donate += 1
            elif remain > 0:
                project.invested_amount += donate.remain
                donate.deactivate()
            else:
                donate.invested_amount += project.remain
                project.deactivate()
            session.add(project)
            session.add(donate)
            await session.commit()
            await session.refresh(project)
            await session.refresh(donate)



