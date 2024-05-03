"""Модуль обработки анкеты"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command 
from aiogram.fsm.context import FSMContext
from states.anketa import Anketa
import keyboards.anketa as kb_anketa

router = Router()

@router.message(Command('anketa'))
async def anketa_handler(msg: Message, state: FSMContext):
    """Обрабатывает команду /anketa"""
    await state.set_state(Anketa.name)
    await msg.answer('Введите ваше имя', reply_markup=kb_anketa.kb_cancel_btn)

    
@router.callback_query(F.data == 'cancel_anketa')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатия кнопки Отмена"""
    await state.clear()
    await callback_query.message.answer('Регистрация отмена')

@router.message(Anketa.name)
async def set_name_by_anketa_handler(msg: Message, state: FSMContext):
    """Обрабатывает ввод имени"""
    await state.update_data(name=msg.text)
    await state.set_state(Anketa.age)
    await msg.answer(
        'Введите ваш возраст', reply_markup=kb_anketa.kb_cancel_back_btn)

@router.callback_query(F.data == 'back_anketa')
async def back_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатие кнопки Назад"""
    current_state = await state.get_state()
    if current_state == Anketa.gender:
        await state.set_state(Anketa.age)
        await callback_query.message.answer(
            'Введите ваш возраст', reply_markup=kb_anketa.kb_cancel_back_btn)
        
    elif current_state == Anketa.age:
        await state.set_state(Anketa.name)
        await callback_query.message.answer(
            "Ведите ваше имя", reply_markup=kb_anketa.kb_cancel_btn)
        
@router.message(Anketa.age)
async def set_age_by_anketa_handler(msg: Message, state: FSMContext):
    """Обрабатываем ввод возраста"""
    try:
       await state.update_data(age=int(msg.text))
    except ValueError:
       await msg.answer('Вы не верно ввели возраст!')
       await msg.answer(
           'Введите ваш возраст', reply_markup=kb_anketa.kb_cancel_back_btn)
       return
    await state.set_state(Anketa.gender)
    await msg.answer(
        'Введите ваш пол', 
        reply_markup=kb_anketa.kb_cancel_back_genders_btn)

@router.callback_query(F.data.startwiht('gender_') and Anketa.gender)
async def set_gender_btn_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатие по кнопкам с полом"""
    gender = {'gender_m':'Мужской', 'gender_w':'Женский'}[callback_query.data]
    await state.update_data(gender=gender)
    await callback_query.message.answer(str(await state.get_data()))
    await state.clear()

@router.message(Anketa.gender)
async def set_gender_txt_by_anketa_handler(msg: Message):
    """Обрабатывает ввод пола"""
    await msg.answer('Нужно пол выбрать кнопкой')