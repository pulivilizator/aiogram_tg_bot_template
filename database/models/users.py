from uuid import UUID

from sqlalchemy import Uuid, text, BigInteger, ForeignKey, Enum as SqlAlchemyEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.enums import Languages
from .base import Base
from .mixins import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=True)

    settings: Mapped['UserSettings'] = relationship(back_populates='user', uselist=False, cascade='all, delete-orphan')

class UserSettings(TimestampMixin, Base):
    __tablename__ = 'users_settings'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    language: Mapped[str] = mapped_column(SqlAlchemyEnum(Languages), nullable=False, default=Languages.EN)
    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    user: Mapped['User'] = relationship(back_populates='settings')