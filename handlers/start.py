from aiogram import types, Dispatcher

async def start_cmd(message: types.Message):
    await message.reply(
        "Привет! Я downloaderPET 🚀\n"
        "Отправь мне ссылку на TikTok, Instagram, VK или YouTube — я попробую скачать и вернуть тебе видео (с водяными знаками, если они есть)."
    )

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=["start"])
