from os import environ
from time import sleep

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import ConnectionError


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


def prepare_message(lesson_info):
    message = ''
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


def main():
    load_dotenv()
    devman_token = environ['DEVMAN_TOKEN']
    telegram_token = environ['TELEGRAM_TOKEN']
    tg_chat_id = environ['TG_CHAT_ID']
    telegram_bot = telegram.Bot(telegram_token)
    get_attempts_time = 6
    attempt_tries = 0
    timestamp = ''
    while True:
        try:
            lesson_info = get_checked_works(devman_token, timestamp)
            timestamp = ''
            if lesson_info['status'] == 'timeout':                
                timestamp = lesson_info['timestamp_to_request']
            else:
                timestamp = lesson_info['last_attempt_timestamp']
                telegram_bot.send_message(
                    tg_chat_id, prepare_message(lesson_info))
        except ConnectionError:
            attempt_tries += 1
            if attempt_tries >= 5:
                print('Ошибка соединения')
                sleep(get_attempts_time)
                attempt_tries = 0


if __name__ == "__main__":

    main()
