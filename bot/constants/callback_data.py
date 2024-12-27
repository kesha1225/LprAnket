from enum import StrEnum, auto


class SimpleCallbackData(StrEnum):
    start_form = auto()
    again = auto()

    yes = auto()
    no = auto()
    skip = auto()

    excel_dump = auto()
