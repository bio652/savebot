from aiogram.fsm.state import StatesGroup, State

class InProcessBlocker(StatesGroup):
    blockmessages = State()
    
class Admin(StatesGroup):
    active = State()
    addchan = State()
    delchan = State()