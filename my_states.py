from aiogram.fsm.state import StatesGroup, State


class Test(StatesGroup):
    menu = State()

class States(StatesGroup):
     # /start - запрос мастер пароля
    first_entering_master_key = State()
    confirm_master_key = State()
    entering_master_key = State()
    
    passed = State()
    entering_service_name = State()
    entering_login = State()
    entering_password = State()