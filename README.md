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

### 5. Запуск через Docker
1. Установите [Docker](https://www.docker.com/get-started/)
2. Переходим в папку со скаченным кодом и запускаем командную строку.
3. Загружаем в командную строку образ из докерхаба
```pycon
docker pull capark74/chekc_works:latest
```
5. Запуск докер контейнера

```pycon
docker run --rm --env TG_BOT_TOKEN='5293067707:AAH....' --env DEVMAN_TOKEN='Token ebbb7.....' --env CHAT_ID=7048... check_works
```

Вы должны увидеть результат:
```pycon
1 INFO Бот перезапущен
```
А также данное сообщение должно появиться в вашем чат боте

