from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButtonPollType
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram import Router

bp = Router()

rmk = ReplyKeyboardRemove()

def profile(text: str | list):
    builder = ReplyKeyboardBuilder()
    
    if isinstance(text, str):
        text = [text]
        
    [builder.button(text=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_Keyboard=True, selective=True)


sub_channel = InlineKeyboardMarkup(inline_keyboard=[
    [
        
        InlineKeyboardButton(text='Подписаться', url='https://t.me/+zMtVTGAmbFtlYjMy')
    ]
])



class Pagination(CallbackData, prefix="pag"):
    action: str
    # page: int


def paginator(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        # InlineKeyboardButton(text="⬅", callback_data=Pagination(action="prev").pack()),
        InlineKeyboardButton(text="➡", callback_data=Pagination(action="next").pack()),
        width=2
    )
    return builder.as_markup()