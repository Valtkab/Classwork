"""Клавиатуры для команды /anketa"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_cancel_btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_anketa')]])

kb_cankel_back_btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='back_anketa'),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_anketa',)]])

kb_cankel_back_genders_btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='back_anketa'),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_anketa',),
    ],[
            InlineKeyboardButton(
            text='Мужской',
            callback_data='gender_m'),
        InlineKeyboardButton(
            text='Женский',
            callback_data='gender_w',),
    ]])
