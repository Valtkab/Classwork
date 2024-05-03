import asyncio
from aiogram import Bot, Dispatcher
from handlers import include_routers

bot = Bot(token="7003052409:AAG1r9XZdCudeVgieMBhvTH8HvSuSCji_n0")
dp = Dispatcher()
router = Router()

class Anketa(StatesGroup):
    name = State()
    age = State()
    gender = State()

@router.message(Command('anketa'))
async def anketa_handler(msg: Message, state: FSMContext):
    await state.set_state(Anketa.name)
    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')]])
    await msg.answer('Введите ваше имя', reply_markup=markup)

@router.callback_query(F.data == 'cancel_anketa')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.answer('Регистрация отмена')

@router.message(Anketa.name)
async def set_name_by_anketa_handler(msg: Message, state: FSMContext):
    await state.update_date(name=msg.text)
    await state.set_state(Anketa.age)
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='set_name_anket'),
        InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa'),]])
    await msg.answer('Введите ваш возраст', reply_markup=markup)

router.callback_query(F.data == 'cancel_anketa')
async def set_name_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    await anketa_handler(callback_query.message, state)

@router.message(Anketa.age)
async def set_name_by_anketa_handler(msg: Message, state: FSMContext):
    try:
       await state.update(age=int(msg.text))
    except ValueError:
       await msg.answer('Вы не верно ввели возраст!')
       markup = InlineKeyboardMarkup(inline_keyboard=[[
          InlineKeyboardButton(text='Назад', callback_data='back_anketa'),
          InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa'),]])
       await msg.answer('Введите ваш возраст', reply_markup=markup)
       return

    await state.set_state(Anketa.gender)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text='Назад', callback_data='back_anketa'),
        InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa'),
        ],[
        InlineKeyboardButton(text='Мужской', callback_data='gender_m'),
        InlineKeyboardButton(text='Женский', callback_data='gender_w'),
        ]])
    await msg.answer('Введите ваш пол', reply_markup=markup)

@router.callback_query(F.data == 'back_anketa')
async def set_age_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Anketa.gender:
        await state.set_state(Anketa.age)
        markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Назад', callback_data='set_name_anket'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa'),]])
        await callback_query.message.answer('Введите ваш возраст', reply_markup=markup)

    elif current_state == Anketa.age:
        await state.set_state(Anketa.name)
        markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa'),]])
        await callback_query.message.answer("Ведите ваше имя", reply_markup=markup)


@router.callback_query(F.data.startwiht('gender_' and Anketa.gender))
async def set_age_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    gender = {'gender_m':'Мужской', 'gender_w':'Женский'}[callback_query.data]
    await state.update_data(gender=gender)
    await callback_query.message.answer(str(await state.get_data()))
    await state.clear()


@router.message(Anketa.gender)
async def set_age_by_anketa_handler(msg: Message, state: FSMContext):
    await msg.answer('Нужно пол выбрать кнопкой')
   
@router.message(Command("start"))
async def start_handler(msg: Message):
    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Спарвка'),
        BotCommand(command='delete', description='Отчислиться'),
    ])

    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вперед', callback_data='next')]
    ])
    await msg.answer(text='Страница 1', reply_markup=inline_markup)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ])
    await callback_query.message.edit_text(
        'Страница 2', reply_markup=inline_markup)



@router.callback_query(F.data == 'back')
async def back_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вперед', callback_data='next')]
    ])
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Страница 1',
        reply_markup=inline_markup)

async def main():
    include_routers(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
