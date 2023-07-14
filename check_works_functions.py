from os import environ
from time import sleep

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, ReadTimeout
from retry import retry


def main():
    load_dotenv()
    devman_token = environ['DEVMAN_TOKEN']
    telegram_token = environ['TELEGRAM_TOKEN']
    tg_chat_id = environ['TG_CHAT_ID']
    telegram_bot = telegram.Bot(telegram_token)
    get_attempts_time = 60
    timestamp = ''
    while True:
        try:
            lesson_info = get_checked_works(devman_token, timestamp)
            timestamp = send_checking_notification(
                telegram_bot, tg_chat_id, lesson_info)
        except ReadTimeout:
            print('Сервер не отвечает')
        except ConnectionError:
            print('Ошибка соединения')
            sleep(get_attempts_time)


@retry(ConnectionError, tries=3, delay=1, backoff=5)
def get_checked_works(devman_token, timestamp):
    headers = {
        'Authorization': f'Token {devman_token}',
    }
    params = {
        'timestamp': timestamp,
    }
    url = 'https://dvmn.org/api/long_polling/'
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    lesson_info = response.json()
    return lesson_info


def send_checking_notification(telegram_bot, tg_chat_id, lesson_info):
    timestamp = ''
    if lesson_info['status'] == 'timeout':
        print('Сервер не отвечает')
        timestamp = lesson_info['timestamp_to_request']
    else:
        timestamp = lesson_info['last_attempt_timestamp']
        telegram_bot.send_message(tg_chat_id, prepare_message(lesson_info))
    return timestamp


def prepare_message(lesson_info):
    for lesson in lesson_info['new_attempts']:
        lesson_title = lesson['lesson_title']
        lesson_url = lesson['lesson_url']
        if lesson['is_negative']:
            checking_result = 'К сожалению, в работе нашлись ошибки'
        else:
            checking_result = 'Преподавателю всё понравилось, можно приступать к следующему уроку'
    message = f'''У вас проверили работу {lesson_title}
                {lesson_url}
                {checking_result}
    '''
    return message


if __name__ == "__main__":

    main()