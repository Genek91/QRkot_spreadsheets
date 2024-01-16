from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def count(
    obj: Union[CharityProject, Donation],
    objs_to_count: Union[list[CharityProject], list[Donation]],
    session: AsyncSession
) -> None:
    objs_to_count = objs_to_count.scalars().all()
    obj_amount = obj.full_amount - obj.invested_amount

    for obj_to_count in objs_to_count:
        need_amount = obj_to_count.full_amount - obj_to_count.invested_amount

        if obj_amount > need_amount:
            obj_to_count.invested_amount = obj_to_count.full_amount
            obj_amount = obj_amount - need_amount
            obj.invested_amount = obj.full_amount - obj_amount
            saving_data(obj_to_count)
        elif obj_amount < need_amount:
            obj_to_count.invested_amount = (
                obj_to_count.invested_amount + obj_amount
            )
            obj_amount = 0
            obj.invested_amount = obj.full_amount
            saving_data(obj)
        else:
            obj_to_count.invested_amount = obj_to_count.full_amount
            saving_data(obj_to_count)
            obj_amount = 0
            obj.invested_amount = obj.full_amount
            saving_data(obj)

        session.add(obj_to_count)

        if obj_amount == 0:
            break


def saving_data(
    saving_obj: Union[CharityProject, Donation]
) -> None:
    saving_obj.fully_invested = True
    saving_obj.close_date = datetime.now()


async def create_investment(
    obj: Union[CharityProject, Donation],
    session: AsyncSession
) -> None:
    if isinstance(obj, Donation):
        all_project = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == False  # noqa
            )
        )
        count(obj, all_project, session)
    else:
        all_donation = await session.execute(
            select(Donation).where(
                CharityProject.fully_invested == False  # noqa
            )
        )
        count(obj, all_donation, session)

    await session.commit()
    await session.refresh(obj)
