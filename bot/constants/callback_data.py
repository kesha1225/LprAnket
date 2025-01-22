from enum import StrEnum, auto


class SimpleCallbackData(StrEnum):
    start_form = auto()
    again = auto()

    yes = auto()
    no = auto()
    skip = auto()

    excel_dump = auto()

    cancel = auto()


class BroadcastCallbackData(StrEnum):
    start_broadcast = "start_broadcast"

    broadcast_to_all = "broadcast_to_all"
    broadcast_to_meet_wishers = "broadcast_to_meet_wishers"

    confirm_broadcast = "confirm_broadcast"
    cancel_broadcast = "cancel_broadcast"
