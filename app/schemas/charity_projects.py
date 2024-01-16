from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: int = Field(..., gt=0)


class CharityProjectCreate(CharityProjectBase):

    @validator('name', 'description', 'full_amount')
    def fields_cannot_be_none(cls, value):
        if value == '':
            raise ValueError('Поле не может быть пустым!')

        return value


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[int] = Field(None, gt=0)

    @validator('name', 'description', 'full_amount')
    def fields_cannot_be_none(cls, value):
        if value == '':
            raise ValueError('Поле не может быть пустым!')

        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
