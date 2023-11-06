from pprint import pprint
from datetime import date
from telebot import types
from colorama import init, Fore
from colorama import Style

from API.get_API import get_api
from API.get_lat import latitude_and_longitude
from API.get_forecast import forecast
from config import dict_form_eng_to_rus, TOKEN, MASSAGE_START
from API.get_all_info import get_result
from API.for_DB import put_to_db, how_many_spins, minus_spin, check_users
import telebot


API = TOKEN
bot = telebot.TeleBot(API)
city=""
dct_user={
    "free spin":True,
    'wait_cite':False,
    'wait_name':False,
    'name': "",
}

def get_forecast(cite:str):
    what_city = cite

    api = get_api(what_city)

    # Получаем координаты
    miron = latitude_and_longitude(api)


    if miron != "Error":
        # Получаем полный прогноз на день
        latitude, longitude = miron
        current_date = date.today()
        current_date_2 = current_date
        current_date_2 = str(current_date_2)
        current_date_2 = current_date_2.replace("-", "")

        forecast_2 = forecast(current_date_2, latitude, longitude)

        result = get_result(forecast_2, current_date, dict_form_eng_to_rus)
        return result
    else:
        return "Я тебя не понимаю. Пожалуйста повтори."




@bot.message_handler(commands=["start"])  # декоратор который реагирует на команду старт
def start(message):
    create_or_not=check_users(message.from_user.id)
    if create_or_not:
        result = put_to_db(message.from_user.id)
        table = types.ReplyKeyboardMarkup(resize_keyboard=True)  # получаем разметку поля
        item_1 = types.KeyboardButton("☀️Получить прогноз погоды.☁️️")  # получаем кнопки которые будут в телеге
        item_2 = types.KeyboardButton("Регистратия пользователя")
        table.add(item_1)  # делаем их расположение по иерархии
        table.add(item_2)
        mes=MASSAGE_START.format(username=message.from_user.first_name)  # настраиваем сообщение которое будет выводить бот
        bot.send_message(message.chat.id, mes, reply_markup=table)  # выводим сообщение с таблицей
    else:
        table = types.ReplyKeyboardMarkup(resize_keyboard=True)  # получаем разметку поля
        item_1 = types.KeyboardButton("☀️Получить прогноз погоды.☁️️")  # получаем кнопки которые будут в телеге
        item_2 = types.KeyboardButton("Регистратия пользователя")
        table.add(item_1)  # делаем их расположение по иерархии
        table.add(item_2)
        mes=MASSAGE_START.format(username=message.from_user.first_name)  # настраиваем сообщение которое будет выводить бот
        bot.send_message(message.chat.id, mes, reply_markup=table)  # выводим сообщение с таблицей

@bot.message_handler(content_types=['text'])
def get_forecast_for_today(message):
    user_message = message.text
    if user_message == "☀️Получить прогноз погоды.☁️️":
        count=how_many_spins(message.from_user.id)
        if count>0:
            mes = "🏘️Введите нужный вам город🏘️: "
            bot.send_message(message.chat.id, mes)
            minus_spin(message.from_user.id)
            dct_user['wait_cite']= True
        else:
            bot.send_message(message.chat.id, "Упс, у вас закончились фри спины. Чтобы продолжить пользоваться ботом-зарегестрируйтесь.")
    elif user_message == "☁️⚡💦Хотите получить повторный прогноз погоды?☁️⚡💦":
        count=how_many_spins(message.from_user.id)
        if count>0:
            mes = "🏘️Введите нужный вам город🏘️: "
            bot.send_message(message.chat.id, mes)
            minus_spin(message.from_user.id)
            dct_user['wait_cite']= True
        else:
            bot.send_message(message.chat.id, "Упс, у вас закончились фри спины. Чтобы продолжить пользоваться ботом-зарегестрируйтесь.")
    elif user_message == "Регистратия пользователя":
        bot.send_message(message.chat.id,"Введите ваше имя: ")
        dct_user['wait_name']=True
    else:
        if dct_user["wait_cite"]:
            table = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1 = types.KeyboardButton("Регистратия пользователя")
            item_2 = types.KeyboardButton("☁️⚡💦Хотите получить повторный прогноз погоды?☁️⚡💦")
            table.add(item_2, item_1)
            city = message.text
            result = get_forecast(city)
            bot.send_message(message.chat.id, result, reply_markup=table)
            dct_user["wait_cite"]=False
        elif dct_user["wait_name"]:
            dct_user['name']=user_message
            put_to_db(message.from_user.id, users_name=user_message, registration=True)
            dct_user["wait_name"]=False
            bot.send_message(message.chat.id, 'Регистрация пользователя произведена успешно. Удачного пользования)))')
        else:
            bot.send_message(message.chat.id, 'Я тебя не понимаю')




if __name__ == "__main__":
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Бот успешно запущен.")
    bot.polling(none_stop=True)