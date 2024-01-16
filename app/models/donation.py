from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.base import BaseDonationCharityProject


class Donation(BaseDonationCharityProject, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
