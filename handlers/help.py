from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: Message):
    text = (
        "Привет! Я бот downloaderPET.\n\n"
        "Отправь мне ссылку на видео с TikTok, Instagram, VK или YouTube — я скачаю его и отправлю тебе.\n\n"
        "Команды:\n"
        "/start — приветствие\n"
        "/help — показать это сообщение"
    )
    await message.reply(text)

@router.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Привет! Я бот downloaderPET. Отправь ссылку на видео, и я его скачаю.")
