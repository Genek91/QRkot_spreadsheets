from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_invested_amount,
                                check_charity_project_status,
                                check_full_amount, check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_projects import charity_project_crud
from app.schemas.charity_projects import (CharityProjectCreate,
                                          CharityProjectDB,
                                          CharityProjectUpdate)
from app.utils.investment import create_investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_charity_projects = await charity_project_crud.get_multi(session)

    return all_charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    await create_investment(new_charity_project, session)

    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_status(
        charity_project
    )

    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount:
        await check_full_amount(
            charity_project.invested_amount, obj_in.full_amount
        )

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )

    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_invested_amount(
        charity_project
    )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )

    return charity_project
