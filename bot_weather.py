from config import TOKEN, weather_API
import datetime
import requests
import telebot

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands = ["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Якщо ви хочете дізнатись погоду в якомусь місті напишіть погода ")

@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.text.lower() == "погода":
        msg = bot.reply_to(message, "Напишіть назву міста: ")
        bot.register_next_step_handler(msg,send_weather)

def send_weather(message,weather_API = weather_API):
    try:
        emoji_codes = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Хмарно \U00002601",
            "Drizzle": "Дощ \U00002614"
        }
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_API}&units=metric")
        data = r.json()
        city = data["name"]
        current_temperature = data["main"]["temp"]
        weather_decription = data['weather'][0]['main']
        if weather_decription in emoji_codes:
            wd = emoji_codes[weather_decription]
        else:
            wd = "Подивися у вікно \U00001F604"
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        bot.send_message(message.chat.id, f"Зараз {datetime.datetime.now().strftime('%H:%M')} \n"
                                          f"Місто - {city} \n"
                                          f"Температура - {str(current_temperature)[0:2]}°C {wd} \n"
                                          f"Тиск - {pressure} мм.рт.ст \n"
                                          f"Влажність - {humidity}% \n"
                                          f"Пориви вітру - {wind} м/год \n"
                                          f"Час сходу сонця - {sunrise} \n"
                                          f"Час заходу сонця - {sunset}")


    except Exception as ex:
        msg = bot.send_message(message.chat.id, "уточніть назву міста")
        bot.register_next_step_handler(msg, send_weather)


if __name__ == "__main__":
    bot.infinity_polling()