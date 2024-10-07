import random
from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.enums.dice_emoji import DiceEmoji
from filtres.is_admin import IsAdmin
from filtres.is_digit_or_float import CheckForDigit

bp = Router()
мой_айди = 699830381


@bp.message(Command('play'), CheckForDigit())
async def play_the_order(message: Message, command: CommandObject):
    print(message.text)
    print(len(message.text))
    await message.answer(f'Вы успешно купили')