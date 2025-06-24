from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.config import Config
from src.bot.handlers import MessageHandlers
import asyncio

class SupportBot:
    def __init__(self):
        self.config = Config()
        self.bot = Bot(token=self.config.TELEGRAM_TOKEN)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self.handlers = MessageHandlers(self.dp)

    async def start(self):
        await self.dp.start_polling(self.bot)

    def run(self):
        asyncio.run(self.start())