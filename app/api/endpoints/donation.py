from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donations import donation_crud
from app.models import User
from app.schemas.donations import (DonationsAdminDB, DonationsCreate,
                                   DonationsMyDB)
from app.utils.investment import create_investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationsAdminDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations_admin(
    session: AsyncSession = Depends(get_async_session)
):
    all_donations = await donation_crud.get_multi(session)

    return all_donations


@router.get(
    '/my',
    response_model=list[DonationsMyDB],
    response_model_exclude_none=True
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donations = await donation_crud.get_donations_by_user(session, user)

    return donations


@router.post(
    '/',
    response_model=DonationsMyDB,
    response_model_exclude_none=True
)
async def create_new_donation(
    donation: DonationsCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation, session, user)
    await create_investment(new_donation, session)

    return new_donation
