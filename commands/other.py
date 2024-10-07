from aiogram import F, Router, types, Bot
from aiogram.filters import Command, CommandObject, CommandStart, ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated, FSInputFile
from aiogram.enums.dice_emoji import DiceEmoji
from filtres.is_admin import IsAdmin
from filtres.is_digit_or_float import CheckForDigit
from facts.fact import fact
from aiogram.utils.media_group import MediaGroupBuilder
from commands.keyboards import paginator, rmk, Pagination
from aiogram.exceptions import TelegramBadRequest
from configure import config
from contextlib import suppress
import datetime
import wikipedia
from aiogram.fsm.context import FSMContext
import random

bot = Bot(config['token'])
bp = Router()

@bp.message(CommandStart())
async def start(message: Message):
    await message.answer('Bot connected successfully ☑️')
    print(message.from_user)
    await bot.send_message(
        chat_id=config['my_id'],
        text=f'Пользователь --> @{message.from_user.username} запустил бота')

    

# Этот хэндлер будет срабатывать на блокировку бота пользователем
@bp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    await bot.send_message(
        chat_id=config['my_id'],
        text=f'Пользователь --> @{event.from_user.username} заблокировал бота')


@bp.message(Command('random', 'рандом'))
async def random_number(message: Message):
    await message.answer_dice(DiceEmoji.DICE)
    

@bp.message(F.new_chat_members)
async def somebody_added(message: Message):
    for user in message.new_chat_members:
        # проперти full_name берёт сразу имя И фамилию 
        # (на скриншоте выше у юзеров нет фамилии)
        await message.reply(f"Добро пожаловать! {user.username}")



@bp.message(F.text.lower()=='время')
async def time_handler(message: Message):
    delta = datetime.timedelta(hours=3, minutes=0)
    t = (datetime.datetime.now(datetime.timezone.utc) + delta)
    nowtime = t.strftime("%H:%M")
    nowdate = t.strftime("%d.%m.%Y")
    await message.reply(f"{nowtime} | {nowdate}")



@bp.callback_query(Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: Pagination):

    if callback_data.action == "next":
        page = random.choice(fact)
        
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"<b>{page}</b>",
            reply_markup=paginator(page)
        )
    await call.answer()

@bp.message(F.text.lower()=='факт')
async def fact_handler(message: Message):
    await message.answer(f"{random.choice(fact)}", reply_markup=paginator())


@bp.message(F.text.lower()=="вики <text>")
async def wiki_handler(message: Message):
    try:
        await message.answer(str(wikipedia.summary(message.text.lower()[5:])))
    except Exception:
        return "❌ | Запрос некорректный!"



@bp.message(Command('бот'))
async def ping_bot(message: Message):
    # print(message.from_user.id)
    print(message.chat.id)
    # await message.answer('⚙️ In place')


async def edit_msg(message: types.Message):
    await message.edit_text("Так")

@bp.message(Command('help'))
async def commands_help(message: Message):
    await message.reply('https://telegra.ph/Komandy-10-06-3')
   