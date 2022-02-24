from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from peewee import PostgresqlDatabase

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = PostgresqlDatabase(config.DATABASE_NAME, user=config.DATABASE_USER,
                        password=config.DATABASE_PASSWORD, host=config.DATABASE_HOST, port=config.DATABASE_PORT)
