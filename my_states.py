from aiogram.fsm.state import StatesGroup, State


class Test(StatesGroup):
    menu = State()


class States(StatesGroup):
    # /start - запрос мастер пароля
    first_entering_master_key = State()
    entering_master_key = State()
    confirm_master_key = State()

    passed = State()

    entering_all_data = State()
    entering_all_data_change = State()
    entering_data = State()
    entering_data_change = State()

    confirm_deleting_password = State()
