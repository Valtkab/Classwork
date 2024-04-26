"""Пакет с обработчиками событий"""
from aiogram import Dispatcher

from handlers import anketa, start

def include_routers(dp: Dispatcher):
    """Подключает роутеры со всех модулей"""
    dp.include_router(
        start.router,
        anketa.router
    )