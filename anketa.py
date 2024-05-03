"""Наборо состоянии для анкеты"""
from aiogram.fsm.state import State, StatesGroup


class Anketa(StatesGroup):
    """Состояний для анкеты"""
    name = State()
    age = State()
    gender = State()

