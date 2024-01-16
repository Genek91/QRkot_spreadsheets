from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationsBase(BaseModel):
    full_amount: int = Field(..., gt=0)


class DonationsCreate(DonationsBase):
    comment: Optional[str]


class DonationsBaseDB(BaseModel):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationsAdminDB(DonationsBase, DonationsBaseDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    comment: Optional[str]


class DonationsMyDB(DonationsBase, DonationsBaseDB):
    comment: Optional[str]
