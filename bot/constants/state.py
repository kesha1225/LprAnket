from aiogram.fsm.state import State, StatesGroup


class FormGroup(StatesGroup):
    name = State()
    region = State()
    notify = State()
    meetings = State()
    near_politic = State()
    lpr_join = State()
    other = State()


class BroadcastForm(StatesGroup):
    choice_type = State()
    input_message = State()
    input_stop = State()
    confirm = State()
