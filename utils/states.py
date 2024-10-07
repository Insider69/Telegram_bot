from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    Имя = State()
    Возраст = State()
    Пол = State()
    Описание = State()
    photo = State()