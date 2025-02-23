from datetime import datetime

from sqlalchemy import func, DateTime
from sqlalchemy.orm import mapped_column, Mapped


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, onupdate=func.now(), default=func.now())