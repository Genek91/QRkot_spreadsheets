from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_projects import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session
    )

    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)

    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )

    return charity_project


async def check_charity_project_status(
    charity_project: CharityProject
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_charity_project_invested_amount(
    charity_project: CharityProject
) -> None:
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_full_amount(
    charity_project: int,
    obj_in: int
) -> None:
    if charity_project > obj_in:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя делать сумму меньше чем уже было внесено средств'
        )
