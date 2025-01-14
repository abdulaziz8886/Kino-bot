from aiogram.fsm.state import StatesGroup, State

class addmovieForm(StatesGroup):
    kino = State()
    izox = State()
    kod = State()
    final = State()


class deleteForm(StatesGroup):
    delete = State()
