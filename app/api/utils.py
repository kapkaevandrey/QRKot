from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import donation_crud, project_crud


async def investment_process(session: AsyncSession) -> None:
    request = dict(
        attr_name='fully_invested', attr_value=False,
        order_by='create_date', many=True,
    )
    donations = await donation_crud.get_by_attribute(
        session=session, **request
    )
    if not donations:
        return
    projects = await project_crud.get_by_attribute(session=session, **request)
    current_donate = 0
    for project in projects:
        for donation in donations[current_donate:]:
            remain = project.remain - donation.remain
            if remain == 0:
                await project.deactivate()
                await donation.deactivate()
                current_donate += 1
            elif remain > 0:
                project.invested_amount += donation.remain
                await donation.deactivate()
            else:
                donation.invested_amount += project.remain
                await project.deactivate()
            if remain <= 0:
                break
    await project_crud.save(projects, session, many=True)
    await donation_crud.save(donations, session, many=True)
