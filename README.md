
# downloaderPET

Telegram-бот для скачивания видео с TikTok, Instagram, VK и YouTube.  
Пользователь отправляет ссылку на видео — бот скачивает его и отправляет обратно в Telegram.

## Функции

- Скачивание видео с TikTok, Instagram, VK, YouTube
- Отправка видео пользователю в Telegram
- Проверка размера файла (лимит Telegram 50 MB)
- Безопасное использование токена через `.env`
- Поддержка Docker для стабильного запуска

## Структура проекта

```

downloaderPET/
├─ bot.py
├─ handlers/
│   ├─ links.py
│   └─ help.py
├─ utils/
│   └─ downloader.py
├─ downloads/
├─ .env
├─ .gitignore
├─ requirements.txt
├─ Dockerfile
└─ docker-compose.yml

````

- `bot.py` — основной файл запуска бота  
- `handlers/links.py` — обработка ссылок и отправка видео  
- `handlers/help.py` — команды `/start` и `/help`  
- `utils/downloader.py` — скачивание видео через `yt-dlp`  
- `downloads/` — временная папка для сохранения видео  
- `.env` — хранит токен бота (`BOT_TOKEN`)  
- `Dockerfile` и `docker-compose.yml` — для запуска в Docker  

## Установка и запуск локально

1. Клонируем репозиторий:

```bash
git clone https://github.com/yourusername/downloaderPET.git
cd downloaderPET
````

2. Создаем виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Устанавливаем зависимости:

```bash
pip install -r requirements.txt
```

4. Создаем `.env` с токеном:

```
BOT_TOKEN=your_bot_token_here
```

5. Запускаем бота:

```bash
python bot.py
```

---

## Запуск через Docker

1. Собираем образ:

```bash
docker build -t downloaderpet .
```

2. Запускаем контейнер:

```bash
docker run --env-file .env downloaderpet
```

3. Или через docker-compose:

```bash
docker compose up -d
docker compose logs -f
```


