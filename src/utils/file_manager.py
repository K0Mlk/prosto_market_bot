import os
from aiogram.types.input_file import FSInputFile

class FileManager:
    @staticmethod
    async def send_pdf(bot, chat_id, file_path):
        try:
            if not os.path.exists(file_path):
                await bot.send_message(chat_id, "Файл инструкции не найден.")
                return

            document = FSInputFile(file_path, filename=os.path.basename(file_path))
        
            await bot.send_document(
                chat_id=chat_id,
                document=document,
                caption="Инструкция:"
            )
        except Exception as e:
            await bot.send_message(chat_id, f"Ошибка при отправке файла: {e}")
