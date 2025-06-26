from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.config import Config

class Keyboards:
    @staticmethod
    def main_menu():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Технические неполадки", callback_data="technical")],
                [InlineKeyboardButton(text="Вопросы, связанные с качеством продукции", url=Config.SUPPORT_CHAT_LINK)],
                [InlineKeyboardButton(text="Другой вопрос или предложение", url=Config.SUPPORT_CHAT_LINK)],
                [InlineKeyboardButton(text="Подписаться на наш Telegram-канал", url=Config.TELEGRAM_CHANNEL_LINK)]
            ]
        )

    @staticmethod
    def technical_submenu():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Не сканируется штрих-код/Белый экран", callback_data="barcode")],
                [InlineKeyboardButton(text="Черный экран", callback_data="screen")],
                [InlineKeyboardButton(text="Нет связи с банком", callback_data="bank")],
                [InlineKeyboardButton(text="Не нашли проблему", callback_data="not_found")],
                [InlineKeyboardButton(text="В мeню ↩️", callback_data="back_to_menu")]
            ]
        )

    @staticmethod
    def contact_operator():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💬 Написать оператору", url=Config.SUPPORT_CHAT_LINK)]
            ]
        )

    @staticmethod
    def back_to_menu():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="В меню ↩️", callback_data="back_to_menu")]
            ]
        )