import os
import asyncio
import tempfile
import shutil
import logging
from yt_dlp import YoutubeDL
from pathlib import Path

logger = logging.getLogger(__name__)

YTDL_OPTS = {
    "outtmpl": "%(id)s.%(ext)s",
    "format": "best[ext=mp4]/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
}

async def download_video_to_file(url: str, download_dir: str = None):
    if download_dir is None:
        download_dir = tempfile.mkdtemp(prefix="downloaderPET_")
        remove_dir_after = True
    else:
        os.makedirs(download_dir, exist_ok=True)
        remove_dir_after = False

    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(None, _run_yt_dlp, url, download_dir)
        if not result:
            return None, None
        filepath, info = result
        return filepath, info
    except Exception as e:
        logger.exception("download_video_to_file error")
        return None, None

def _run_yt_dlp(url: str, download_dir: str):
    tmpdir = tempfile.mkdtemp(dir=download_dir)
    ytdl_opts = YTDL_OPTS.copy()
    ytdl_opts["outtmpl"] = os.path.join(tmpdir, "%(title).200s-%(id)s.%(ext)s")

    with YoutubeDL(ytdl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            if "entries" in info:
                entry = info["entries"][0]
            else:
                entry = info

            filepath = None
            for fname in os.listdir(tmpdir):
                if fname.lower().endswith((".mp4", ".mkv", ".webm", ".mov", ".flv", ".avi")):
                    filepath = os.path.join(tmpdir, fname)
                    break
            if not filepath:
                if "requested_downloads" in entry and entry["requested_downloads"]:
                    fp = entry["requested_downloads"][0].get("filename")
                    if fp and os.path.exists(fp):
                        filepath = fp
            if not filepath:
                logger.error("Файл не найден после yt-dlp скачать.")
                shutil.rmtree(tmpdir, ignore_errors=True)
                return None
            return filepath, entry
        except Exception as e:
            logger.exception("yt-dlp failed to download")
            shutil.rmtree(tmpdir, ignore_errors=True)
            return None

async def cleanup_file(filepath: str):
    if not filepath:
        return
    try:
        parent = Path(filepath).parent
        if os.path.exists(filepath):
            os.remove(filepath)
        try:
            if parent.exists():
                for _ in parent.iterdir():
                    return
                parent.rmdir()
        except Exception:
            pass
    except Exception:
        logger.exception("cleanup_file error")
