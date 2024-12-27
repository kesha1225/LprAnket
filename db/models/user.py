import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BIGINT

from db.models.base import BaseTable, ServerDefault

if typing.TYPE_CHECKING:
    from db.models.form import FormDB


class TGUser(BaseTable):
    __tablename__ = "tg_user"
    __table_args__ = {"comment": "User in Telegram"}

    tg_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(nullable=True)
    first_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)

    is_bot_blocked: Mapped[bool] = mapped_column(
        default=False, server_default=ServerDefault.false
    )

    forms: Mapped[list["FormDB"]] = relationship(back_populates="user")
