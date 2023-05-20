from asyncio import new_event_loop

from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .config import BOT_CONFIG


# Состояния, в которые может переходить бот
class States(StatesGroup):
    add_request = State()
    add_point = State()
    add_geoloc = State()
    add_pic = State()
    add_description = State()
    choose_building = State()
    choose_building_num = State()
    add_addr = State()
    add_flat = State()
    add_room = State()
    add_phone = State()


# объекты для работы aiogram
exc = executor
loop = new_event_loop()

bot = Bot(BOT_CONFIG.TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.setup_middleware(LoggingMiddleware())
