from emojiflags.lookup import lookup
import telebot
import requests
import logging
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

weather_api_host = os.environ.get("WEATHER_API_HOST")


@bot.message_handler(commands=['start'])
def start(message):
    send_mess = f'Привет {message.from_user.first_name} отправь нужный город или локацию'
    bot.send_message(message.chat.id, send_mess)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    url = f"http://{weather_api_host}/weather/lat={message.location.latitude}&lon={message.location.longitude}"
    resp = requests.get(url).json()
    final_message = f"Город: {resp['weathers']['location'][0]['city']}" \
                    f"{lookup(resp['weathers']['location'][0]['country']['name'])}\n" \
                    f"Температура: {resp['weathers']['temperature']} "
    bot.send_message(message.chat.id, final_message)


@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    url = f"http://{weather_api_host}/weather/q={get_message_bot}"
    try:
        resp = requests.get(url).json()
        final_message = f"Город: {resp['weathers']['location'][0]['city']}" \
                        f"{lookup(resp['weathers']['location'][0]['country']['name'])}\n" \
                        f"Температура: {resp['weathers']['temperature']}"
        bot.send_message(message.chat.id, final_message)
    except Exception:
        bot.send_message(message.chat.id, 'Ошибка\nПопробуйте еще раз')
        logging.exception('')


bot.polling(none_stop=True)
