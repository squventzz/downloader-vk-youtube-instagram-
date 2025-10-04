import os
import logging
from aiogram import types, Router
from aiogram.types import FSInputFile
from utils.downloader import download_video_to_file, cleanup_file

logger = logging.getLogger(__name__)
router = Router()

MAX_SEND_SIZE_BYTES = 50 * 1024 * 1024  

@router.message()
async def handle_links(message: types.Message):
    text = message.text.strip()
    
    if not (text.startswith("http://") or text.startswith("https://")):
        await message.reply("Пожалуйста, отправь ссылку (начинающуюся с http/https).")
        return

    await message.reply("Понял. Начинаю загрузку — это может занять некоторое время... ⏳")

    try:
        filepath, info = await download_video_to_file(text, download_dir="downloads")
        if not filepath:
            await message.reply(
                "Не получилось скачать видео с этой ссылки "
                "(поддерживаемые платформы: TikTok, Instagram, VK, YouTube)."
            )
            return

        size = os.path.getsize(filepath)
        if size > MAX_SEND_SIZE_BYTES:
            await message.reply(
                f"Видео скачано ({int(size/1024/1024)} MB), но это может превышать лимит Telegram."
            )

        video = FSInputFile(filepath)
        await message.reply_video(video, caption=f"Вот видео — источник: {info.get('webpage_url') or text}")

    except Exception as e:
        logger.exception("Ошибка при обработке ссылки")
        await message.reply(f"Произошла ошибка при попытке скачать видео: {e}")

    finally:
        try:
            await cleanup_file(filepath)
        except Exception:
            pass
