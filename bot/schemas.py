import dataclasses

from aiogram.types import TelegramObject


@dataclasses.dataclass
class UserMiddlewareStruct:
    tg_id: int
    language_code: str
    username: str | None
    first_name: str | None
    last_name: str | None

    @classmethod
    def from_aiogram_event(cls, event: TelegramObject) -> "UserMiddlewareStruct":
        return cls(
            tg_id=event.from_user.id,
            language_code=event.from_user.language_code,
            username=event.from_user.username,
            first_name=event.from_user.first_name,
            last_name=event.from_user.last_name,
        )
