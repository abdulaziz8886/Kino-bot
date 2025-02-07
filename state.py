from aiogram.fsm.state import StatesGroup, State

class addmovieForm(StatesGroup):
    kino = State()
    izox = State()
    kod = State()
    final = State()


class deleteForm(StatesGroup):
    delete = State()
    
class reklamaForm(StatesGroup):
    rek = State()
    
class reklamaRAsmFORM(StatesGroup):
    rasm = State()
    izoh = State()


class sentSerForm(StatesGroup):
    state1 = State()


class serialForm(StatesGroup):
    tanlov = State()
    kod = State()
    rasm = State()
    izoh = State()

class addserialFOrm(StatesGroup):
    kino = State()
    izox = State()
    kod = State()
    final = State()
    
