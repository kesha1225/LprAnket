from aiogram.fsm.state import State, StatesGroup


class FormGroup(StatesGroup):
    name = State()
    region = State()
    notify = State()
    meetings = State()
    near_politic = State()
    lpr_join = State()
    other = State()
