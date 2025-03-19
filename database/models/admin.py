import datetime

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, intpk, bigint, created_at, updated_at

from bot.enums import Status


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[intpk]

    chat_id: Mapped[bigint]
    title: Mapped[str]
    username: Mapped[str | None]
    url: Mapped[str]

    status: Mapped[Status] = mapped_column(default=Status.AVAILABLE)

    users: Mapped[list[int]] = mapped_column(JSON, default=list)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class Tournament(Base):
    __tablename__ = "tournaments"

    id: Mapped[intpk]

    name: Mapped[str]
    status: Mapped[Status] = mapped_column(default=Status.AVAILABLE)

    organizer: Mapped[str]
    date: Mapped[datetime.date]
    age: Mapped[str]


class Discipline(Base):
    __tablename__ = "disciplines"

    id: Mapped[intpk]
    tournament_id: Mapped[int] = mapped_column(ForeignKey('tournaments.id'))
    name: Mapped[str]


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[intpk]
    name: Mapped[str]
