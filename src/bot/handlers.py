import os
from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile
from src.bot.keyboards import Keyboards
from src.config import Config
from src.database.models import UserModel
import asyncio

class MessageHandlers:
    WELCOME_TEXT = (
        "Добро пожаловать в службу поддержки магазина «Просто Маркет».\n"
        "Чем я могу вам помочь сегодня? 😊"
    )
    
    CAPTIONS = {
        "barcode": "Если у вас не сканируется штрих-код или экран монитора полностью белый, то выполните следующие действия:",
        "screen": "Если у вас черный экран, то выполните следующие действия:",
        "bank": "Вот документ для решения проблемы с отсутствием связи с банком:",
        "not_found": ""  
    }
    
    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.user_model = UserModel()
        self.register_handlers()
        
        self.handlers_map = {
            "technical": self.handle_technical,
            "barcode": self.handle_technical_subcategory,
            "screen": self.handle_technical_subcategory,
            "bank": self.handle_technical_subcategory,
            "not_found": self.handle_technical_subcategory,
            "back_to_menu": self.handle_back_to_menu
        }

    async def start_command(self, message: types.Message):
        self.user_model.create_user_if_not_exists(
            user_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
        await message.answer(self.WELCOME_TEXT, reply_markup=Keyboards.main_menu())

    async def handle_callback(self, callback: CallbackQuery):
        data = callback.data
        handler = self.handlers_map.get(data)
        
        if handler:
            await handler(callback)
        else:
            await callback.answer("Неизвестная команда")
        
        await callback.answer()

    async def handle_technical(self, callback: CallbackQuery):
        await callback.message.edit_text(
            "Выберите подкатегорию",
            reply_markup=Keyboards.technical_submenu()
        )

    async def handle_technical_subcategory(self, callback: CallbackQuery):
        file_key = callback.data
        pdf_path = Config.PDF_MAP.get(file_key)
        
        await callback.message.delete()
        
        wait_message = await callback.message.answer("Ожидайте...😊")
        
        try:
            if file_key == "not_found":
                
                message_text = (
                    "Если вы не нашли свою проблему, позвоните по номеру:\n"
                    "📞 +7 (927) 043-54-99"
                )
                
                await callback.message.answer(
                    message_text,
                    reply_markup=Keyboards.back_to_menu()
                )
            else:
                if not pdf_path:
                    raise FileNotFoundError(f"Файл не найден: {pdf_path}")
                
                document = FSInputFile(pdf_path, filename=os.path.basename(pdf_path))
                
                caption = self.CAPTIONS.get(file_key, "Выполните следующие действия:")
                
                await callback.bot.send_document(
                    chat_id=callback.message.chat.id,
                    document=document,
                    caption=caption,
                    reply_markup=Keyboards.back_to_menu()
                )
            
            self.user_model.log_request(
                user_id=callback.from_user.id,
                category='Технические неполадки',
                subcategory=file_key
            )
            
        except Exception as e:
            await callback.message.answer(
                f"Ошибка: {str(e)}",
                reply_markup=Keyboards.back_to_menu()
            )
        
        if wait_message:
            await wait_message.delete()

    async def handle_back_to_menu(self, callback: CallbackQuery):
        
        await callback.message.delete()
        
        await callback.message.answer(
            self.WELCOME_TEXT,
            reply_markup=Keyboards.main_menu()
        )

    def register_handlers(self):
        self.dp.message.register(self.start_command, Command("start"))
        self.dp.callback_query.register(self.handle_callback)