from aiogram import Router, filters, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from commands.keyboards import profile, rmk 
from utils.states import Form
from configure import config

bp = Router()

@bp.message(Command('profile', 'профиль'))
async def fill_profile(message: Message,  state: FSMContext):
    # if message.bot.id == message.bot.id:
        await state.set_state(Form.Имя)
        await message.answer(
            'Введи свое имя',
            reply_markup=profile(message.from_user.first_name)
        )
    # else:
    #     await message.reply('⚠️ Warning --> Лучше напиши сюда @Moarte_sBot')


@bp.message(Form.Имя)
async def form_name(message: Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer('⚠️ Warning --> Некорректное имя')
    else:
        await state.update_data(Имя=message.text)
        await state.set_state(Form.Возраст)
        await message.answer('Введи свой возраст', reply_markup=rmk)
            

@bp.message(Form.Возраст)
async def form_age(message: Message, state: FSMContext):
    try:
        if message.text.isdigit() and int(message.text) >= 18:
            await state.update_data(Возраст=message.text)
            await state.set_state(Form.Пол)
            await message.answer('Введи свой гендер', reply_markup=profile(['Парень', 'Девушка']))
        
        elif int(message.text) >= 18:
            await state.update_data(age=message.text)
            await state.set_state(Form.Пол)
            await message.answer('Введи свой гендер', reply_markup=profile(['Парень', 'Девушка']))
        
            
        else:
            await state.clear()
            await message.reply('⚠️ Warning --> К сожалению подать заявку не получится 🔞', reply_markup=rmk)
            
    except Exception:
        pass
    
@bp.message(Form.Пол, F.text.casefold().in_(['парень', 'девушка']))
async def form_sex(message: Message, state: FSMContext):
    await state.update_data(Пол=message.text)
    await state.set_state(Form.Описание)
    await message.answer(
        '📝 Охарактеризуй себя 3 словами.\nПиши все одним сообщением', reply_markup=rmk)
    
@bp.message(Form.Пол)
async def incorrect_form_sex(message: Message, state: FSMContext):
    await message.answer('⚠️ Warning --> Нажми на кнопку')
    
    
@bp.message(Form.Описание)
async def form_about(message: Message, state: FSMContext):
    if len(message.text.lower()) > 5:
        await state.update_data(Описание=message.text)
        await state.set_state(Form.photo)
        await message.answer('Отправь свою фотографию', reply_markup=rmk)
    else:
        await message.answer(
            '⚠️ Warning --> Слишком короткое описание')
    

@bp.message(Form.photo, F.photo)
async def form_photo(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    description_users = await state.get_data()
    await state.clear()
    
    list_users = []
    [
        list_users.append(f'{value}')
        for key, value in description_users.items()
    ]
    
    await message.answer_photo(
        photo_file_id,
        '\n'.join(list_users)
    )
    
@bp.message(Form.photo, ~F.photo)
async def incorrect_form_photo(message: Message, state: FSMContext):
    await message.answer('⚠️ Warning --> Отправь фото')
    