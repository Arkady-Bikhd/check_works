# Сервис сообщений о проверке работ

Это чат бот, который отсылает уведомления о статусе проверки уроков на обучающей платформе [Devman](https://dvmn.org/)

## Установка

Установить зависимости:

`pip install -r requirements.txt`

Для хранения переменных окружения создать файл `.env`:

```
DEVMAN_TOKEN=<YOUR_DEVMAN_TOKEN>
TELEGRAM_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
TELEGRAM_CHAT_ID=<YOUR_CHAT_ID_ON_TELEGRAM>
```
## Запуск

Для запуска бота написать в консоле

`python check_notification.py`
