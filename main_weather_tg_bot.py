import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Salem men HAWA-RAYI botiman.\n\nSiz jasaytug'in qala yamasa rayon atin jazin:")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer("Ja'rdem ushin adminge xabarlasin:\n@r_on_in")

@dp.message_handler(commands=["dagaza"])
async def dagaza_command(message: types.Message):
    await message.answer("Dag'aza ushin adminge xabarlasin:\n@r_on_in")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ashiq aspan \U00002600",
        "Clouds": "Bultli \U00002601",
        "Rain": "Jawın \U00002614",
        "Drizzle": "Jawın \U00002614",
        "Thunderstorm": "Dúbeley \U000026A1",
        "Snow": "Qar \U0001F328",
        "Mist": "Tuman \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Áynekten sirtqa qaran, ol jerda hawa rayı qandaylıǵın tusinbey atpan!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Qalada hawa-rayi: {city}\nTemperatura: {cur_weather}C° {wd}\n"
              f"Na'mlik: {humidity}%\nBasim: {pressure} мм.рт.ст\nSamal: {wind} м/с\n"
              f"Quyash shig'iwi: {sunrise_timestamp}\nQuyash batiwi: {sunset_timestamp}\nKu'n dawamilig'i: {length_of_the_day}\n"
              f"***Ku'niniz jaqsi o'tsin!***"
              )

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)