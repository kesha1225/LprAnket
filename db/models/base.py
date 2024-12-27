import datetime

from uuid import UUID, uuid4

from sqlalchemy import text, DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    validates,
    DeclarativeBase,
    declarative_base,
)

from bot.time_utils import get_utcnow

Base = declarative_base()


class ServerDefault:
    true = "true"
    false = "false"
    empty_dict = "{}"
    now = text("CURRENT_TIMESTAMP")


class OnDelete:
    cascade = "CASCADE"
    set_null = "SET NULL"
    restrict = "RESTRICT"


class BaseTable(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utcnow,
        server_default=ServerDefault.now,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utcnow,
        server_default=ServerDefault.now,
        onupdate=get_utcnow,
        server_onupdate=ServerDefault.now,
    )

    @validates("created_at", "updated_at")
    def validate_tz_info(self, _: str, value: datetime.datetime) -> datetime.datetime:
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value
