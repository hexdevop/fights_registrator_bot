from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, intpk, bigint, created_at


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]

    user_id: Mapped[bigint]
    username: Mapped[str]
    lang_code: Mapped[str]

    initials: Mapped[str]
    coach_initials: Mapped[str]

    date: Mapped[str]
    gender: Mapped[int]
    weight: Mapped[str]

    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'))
    discipline_id: Mapped[int] = mapped_column(ForeignKey('disciplines.id'))
    region_id: Mapped[int] = mapped_column(ForeignKey('regions.id'))

    created_at: Mapped[created_at]
