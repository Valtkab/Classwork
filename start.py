"""Модуль обработки анкеты"""
from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.anketa import Anketa
import keyboard.anketa as kb_anketa

router = Router()

