import typing

from bot.constants.callback_data import SimpleCallbackData


def get_bool_from_callback_data(data: SimpleCallbackData) -> bool | typing.NoReturn:
    match data:
        case SimpleCallbackData.yes:
            return True
        case SimpleCallbackData.no:
            return False
        case _:
            raise ValueError(f"Invalid callback data: {data}")


def get_text_bool(obj: bool) -> str:
    match obj:
        case True:
            return "Да"
        case False:
            return "Нет"
        case _:
            ValueError(f"bad type for bool {obj}")
