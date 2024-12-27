import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from db.models.base import BaseTable, OnDelete

if typing.TYPE_CHECKING:
    from db.models.user import TGUser


class FormDB(BaseTable):
    __tablename__ = "user_form"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_tg_id: Mapped[int] = mapped_column(
        ForeignKey("tg_user.tg_id", ondelete=OnDelete.cascade)
    )

    user: Mapped["TGUser"] = relationship(back_populates="forms")

    name: Mapped[str] = mapped_column(nullable=False)
    region: Mapped[str] = mapped_column(nullable=False)
    notify: Mapped[bool] = mapped_column(nullable=False)
    meetings: Mapped[bool] = mapped_column(nullable=False)
    near_politic: Mapped[bool] = mapped_column(nullable=False)
    lpr_join: Mapped[bool] = mapped_column(nullable=False)
    other: Mapped[str | None] = mapped_column(nullable=True)
