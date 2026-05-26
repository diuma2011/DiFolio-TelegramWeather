import telebot
import requests
import json
from m_buttons import *
import MOD_VisualCrossingWeather as GEOAPI1
import MOD_OpenMeteo as GEOAPI2
from MOD_OpenMeteo import WEATHER_CODES, WIND_DIRS, windir


adminlist=[5581026055]
currently_in_admin={}
loaded_chats=[]
loaded_users={}
loaded_locations=[]

zaprosov=0

token="не дождёшься дундук"
with open("TOKEN.txt","r")as f:
    token=f.read().strip()
apikey="фиг тебе"
with open("APIKEY.txt","r")as f:
    apikey=f.read().strip()


def JSON_load_chats():
    global loaded_chats,loaded_users,zaprosov,loaded_locations
    with open("database.json","r") as f:
        jsn=json.load(f)
        loaded_chats=jsn["registrated_chat_ids"]
        for e in jsn["verify_users"]:
            loaded_users[e]=None
        zaprosov=jsn["zap"]
        loaded_locations=jsn["loaded_L"]
def add_chat(message):
    if isinstance(message,int):
        if message not in loaded_chats:
            print("Новый зареганный чат!: ",message)
            loaded_chats.append(message)
    else:
        if message.chat.id not in loaded_chats:
            print("Новый зареганный чат!: ",message.chat.id)
            loaded_chats.append(message.chat.id)
def JSON_save():
    with open("database.json","w") as f:
        json.dump({"registrated_chat_ids":loaded_chats,"verify_users":list(loaded_users.keys()),"zap":zaprosov,"loaded_L":loaded_locations},f)


try:
    JSON_load_chats()
except KeyError as e: print("Не получилось получить",e)
except Exception as e: print(e)
bot = telebot.TeleBot(token)

koturl='https://api.thecatapi.com/v1/images/search'

def msg(id,text,**qwargs):
    bot.send_message(id,text,**qwargs)

## Админка и нон-админка
def check_nonadmin(message):
    return message.from_user.id in adminlist and message.from_user.id not in currently_in_admin
def check_admin(message):
    return message.from_user.id in adminlist and message.from_user.id in currently_in_admin

def aboutMe(id):
    msg(id,"""❓ О проекте
    Проект "Weather Bot | Бот Проект" был создан для защиты проекта по Uchi.Doma
    Данный мини-проект содержит несколько интерактивных способов получения информации о погоде,
    да и само оно создано ради проверки знаний и тестировании бота на телеграмм.
    В проекте можно заметить API погоды, работу бота телеги, вывод в формат JSON.
    А также бот собирает данные, чтобы как раз работа с ботом было комфортнее :D""")

### НАЧАЛО КОМАНД

# Админка
@bot.message_handler(commands=["admin"])
def adminka(m):
    if m.from_user.id in loaded_users:
        add_chat(m)
        if check_nonadmin(m):
            msg(m.chat.id,f"USER: {m.from_user.id}\n😎 Админ панель:",reply_markup=adminKeyboard)
            currently_in_admin[m.from_user.id]="idle"
            # bot.stop_bot()
        else:
            print("караул! какой-то",m.from_user.id,m.from_user.username,"в курсе про админку!")

@bot.message_handler(regexp="Остановка бота")
def stopBot(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
        if check_admin(message):
            msg(message.chat.id,"❌ Отключаем бота...")
            bot.stop_bot()

@bot.message_handler(regexp="Сообщение всем")
def messageToAl(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
        if check_admin(message):
            msg(message.chat.id,"💬 Введите сообщение\nВ противном случае напишите /stop",reply_markup=adminKeyboardMessage)
            currently_in_admin[message.from_user.id]="shogochit"

@bot.message_handler(regexp="JSON меню")
def jsonoptions(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
        if check_admin(message):
            msg(message.chat.id,"🟧 Меню JSON",reply_markup=adminKeyboardJSON)
            currently_in_admin[message.from_user.id]="json"

@bot.message_handler(regexp="Обновить датабазу JSON")
def json_upd(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
        if check_admin(message) and currently_in_admin[message.from_user.id]=="json":
            JSON_save()
            msg(message.chat.id,"🔺 Данные JSON обоновлены дистанционно!")

@bot.message_handler(regexp="Закрыть админ сессию")
def closeAdmin(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
        if check_admin(message):
            msg(message.chat.id,"❎ Завершаем вашу сессию админки",reply_markup=menuKeyboard)
            currently_in_admin.pop(message.from_user.id)

@bot.message_handler(regexp="Текущая погода в разных местах")
def unreleasedfeature(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
        msg(message.chat.id,"К сожалению, данная функция не реализована...")

def sbot(m):
    if m.from_user.id not in loaded_users:
        msg(m.chat.id,"👀 Привет, этот бот собирает погоду в городе/месте и возращает результаты.\nЭтот бот был создан для защиты проекта по Uchi Doma (всё ещё в разработке)\nБот собирает данные о пользователях, чтобы работа бота была корректной\nПодтвердите своё согласие на сбор данных (щас оно ничего не собирает)",reply_markup=preKeyboard)
    else:
        msg(m.chat.id,"🗺 Меню приложения",reply_markup=menuKeyboard)
@bot.message_handler(commands=["start","menu"])
def startBot(m):
    sbot(m)
@bot.message_handler(regexp="Меню")
def startBot2(m):
    sbot(m)

# Обработчики текста
@bot.message_handler(regexp="Подтверждаю")
def verify(message):
    add_chat(message)
    if message.from_user.id not in loaded_users.keys():
        loaded_users[message.from_user.id]="idle"
        msg(message.chat.id,"😉 ОК",reply_markup=menuKeyboard)
    else:
        msg(message.chat.id,"☺ Уже не нужно, вы уже в базе данных :)\nЗато мы не Макс))\n(●'◡'●)")

@bot.message_handler(regexp="Что собирает приложение")
def whatwecollecting(message):
    if not check_admin(message):
        msg(message.chat.id,"🤔 Что собирает этот бот:\n*После подтверждения:*\nВаш айди и айди чата будут отправлены в датабазу на сервере\n\nПри получении погоды:\nМы будем использовать геолокацию для быстрого приёма погоды\nА также мы будем хранить информацию погоды о городе/месте, которую вы захотите узнать.\nЭти данные будут использоваться в отдельном блоке 'Текущая погода в разных местах' и при будущих обращениях к этому месту, что оптимизирует время\n\nИ пока что всё. Данные будут использоваться во имя проекта и я сам короче законопослушный")

@bot.message_handler(commands=["about"])
def aboutMe1(m):
    if m.from_user.id in loaded_users:
        add_chat(m)
        aboutMe(m)

@bot.message_handler(regexp="О проекте")
def aboutMe2(m):
    if m.from_user.id in loaded_users:
        add_chat(m)
        aboutMe(m.from_user.id)

def s(m):
    if m.from_user.id in loaded_users:
        add_chat(m)
        msg(m.chat.id,f"📊 Статистика\nСделано запросов за всё время: {zaprosov}\nВсего мест в датабазе: {len(loaded_locations)}\nКол-во чатов: {len(loaded_chats)}\nЮзеров в боте: {len(loaded_users)}")

@bot.message_handler(commands=["curinfo"])
def statistika(m):
    s(m)
@bot.message_handler(regexp="Статистика")
def statistika2(m):
    s(m)
@bot.message_handler(commands=["stop"])
def stopMessageToAll(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
        if check_admin(message) and currently_in_admin[message.from_user.id]=="shogochit":
            msg(message.chat.id,"⭕ Отменяем действие",reply_markup=adminKeyboard)
            currently_in_admin[message.from_user.id]="idle"


@bot.message_handler(regexp="Назад")
def back(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
        if check_admin(message):
            if currently_in_admin[message.from_user.id]=="json":
                currently_in_admin[message.from_user.id]="idle"
                msg(message.chat.id,"💨 Возращаемся обратно",reply_markup=adminKeyboard)

def help(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
        el=message.text.split(" ")
        razdel=0
        if len(el):
            try:
                razdel=int(el[1])
                if not 0<=razdel<=8:
                    msg(message.chat.id,"🛑 Недопустимое значение после команды")
                    return
            except:
                razdel=0
        try:
            with open(f"helpRazdel\\help{razdel}.txt",encoding="utf-8") as f:
                msg(message.chat.id,f.read())
        except Exception as e:
            msg(message.chat.id,"💀 Не удалось открыть Помощь")
            print(e)

@bot.message_handler(regexp="Помощь")
def help1(m):
    help(m)
@bot.message_handler(commands=["help"])
def help2(m):
    help(m)

# Остальной текст

def LocationByLatLon(id,lat,lon):
    global zaprosov
    add_chat(id)
    success=False
    msg(id,"Вбиваем...")
    try:
        collected=GEOAPI1.get_data_with_pos(lat,lon,"next24hours")
    except GEOAPI1.LocationNoFound:
        msg(id, "🏳 Локация не найдена")
    except GEOAPI1.InvalidLocationExpression:
        msg(id, "🏳 Локация некорректна")
    except GEOAPI1.TooLongURL:
        msg(id, "🏳 Ссылка слишком длинная")
    except GEOAPI1.InternalServerError:
        msg(id, "👁 Произошла северная ошибка на стороне VisualCrossingWeather")
    except GEOAPI1.DailyLimit:
        msg(id, "👁 Ежедневный лимит на стороне VisualCrossingWeather закончился")
    except GEOAPI1.VCWAPIError as e:
        msg(id, "👁 Произошла некая ошибка при связи с VisualCrossingWeather")
        print(e)
    else:
        success=True
        zaprosov+=1
        json=collected
        loaded_locations.append({"provider":"visualcrossing"}|json)
        day=0

        msg(id,json["resolvedAddress"])

        msg(id,"СЕГОДНЯ:\nТемпература: {temp}\nВлажность: {humidity}%\nСкорость ветра: {ws} км в час\nНаправление ветра: {wd}\nПогода: {conditions}\n{desc}".format(
            temp=f"{json["days"][day]["tempmin"]}°C-{json["days"][day]["tempmax"]}°C",humidity=json["days"][day]["humidity"],conditions=json["days"][day]["conditions"],desc=json["days"][day]["description"],ws=json["days"][day]["windspeed"],wd=windir(json["days"][day]["winddir"])))

        day=1
        msg(id,"ЗАВТРА:\nТемпература: {temp}\nВлажность: {humidity}%\nСкорость ветра: {ws} км в час\nНаправление ветра: {wd}\nПогода: {conditions}\n{desc}".format(
            temp=f"{json["days"][day]["tempmin"]}°C-{json["days"][day]["tempmax"]}°C",humidity=json["days"][day]["humidity"],conditions=json["days"][day]["conditions"],desc=json["days"][day]["description"],ws=json["days"][day]["windspeed"],wd=windir(json["days"][day]["winddir"])))
        
        msg(id,"СЕЙЧАС:\nТемпература: {temp}\nВлажность: {humidity}%\nСкорость ветра: {ws} км в час\nНаправление ветра: {wd}\nВот такие пироги!".format(
            temp=f"{json["currentConditions"]["temp"]}°C",humidity=json["currentConditions"]["humidity"],ws=json["currentConditions"]["windspeed"],wd=windir(json["currentConditions"]["winddir"])))
    if success:return
    msg(id,"👁 Пробиваем в OpenMeteo")
    try:
        json=GEOAPI2.get_data_with_pos(lat,lon,daily="weather_code,temperature_2m_max,temperature_2m_min,wind_direction_10m_dominant",current="temperature_2m,relative_humidity_2m,weather_code,wind_direction_10m,wind_speed_10m",timezone="auto",forecast_days=2)
        loaded_locations.append({"provider":"openmeteo"}|json)
        day=0

        msg(id,"СЕГОДНЯ:\nТемпература: {temp}\nВлажность: {humidity}\nСкорость ветра: {ws} км в час\nНаправление ветра: {wd}\nПогода: {conditions}\n{desc}".format(
            temp=f"{json["daily"]["temperature_2m_min"][day]}°C-{json["daily"]["temperature_2m_max"][day]}°C",humidity="Нету",conditions=WEATHER_CODES[json["daily"]["weather_code"][day]],desc="Вот такие пироги!",ws="Нету",wd=json["daily"]["wind_direction_10m_dominant"][day]))
        day=1
        msg(id,"ЗАВТРА:\nТемпература: {temp}\nВлажность: {humidity}\nСкорость ветра: {ws} км в час\nНаправление ветра: {wd}\nПогода: {conditions}\n{desc}".format(
            temp=f"{json["daily"]["temperature_2m_min"][day]}°C-{json["daily"]["temperature_2m_max"][day]}°C",humidity="Нету",conditions=WEATHER_CODES[json["daily"]["weather_code"][day]],desc="Вот такие пироги!",ws="Нету",wd=json["daily"]["wind_direction_10m_dominant"][day]))
        msg(id,"СЕЙЧАС:\nТемпература: {temp}\nВлажность: {humidity}\nСкорость ветра: {ws} км в час\nНаправление ветра: {wd}\nПогода: {conditions}\n{desc}".format(
            temp=f"{json["current"]["temperature_2m"]}°C",humidity=str(json["current"]["relative_humidity_2m"])+"%",conditions=WEATHER_CODES[json["current"]["weather_code"]],desc="Вот такие пироги!",ws=json["current"]["wind_speed_10m"],wd=json["current"]["wind_direction_10m"]))
    except Exception as e:
        msg(id, "👁 Произошла некая ошибка при связи с OpenMeteo")
        print(e)
def LocationByName(id,name):
    global zaprosov
    add_chat(id)
    success=False
    msg(id,"Вбиваем...")
    try:
        collected=GEOAPI1.get_data_with_name(name,"next24hours")
    except GEOAPI1.LocationNoFound:
        msg(id, "🏳 Локация не найдена")
    except GEOAPI1.InvalidLocationExpression:
        msg(id, "🏳 Локация некорректна")
    except GEOAPI1.InvalidZipCode:
        msg(id, "🏳 Такого американского почтового индекса нет!")
    except GEOAPI1.TooLongURL:
        msg(id, "🏳 Ссылка слишком длинная")
    except GEOAPI1.InternalServerError:
        msg(id, "👁 Произошла северная ошибка на стороне VisualCrossingWeather")
    except GEOAPI1.DailyLimit:
        msg(id, "👁 Ежедневный лимит на стороне VisualCrossingWeather закончился")
    except GEOAPI1.VCWAPIError as e:
        msg(id, "👁 Произошла некая ошибка при связи с VisualCrossingWeather")
        print(e)
    else:
        success=True
        zaprosov+=1
        json=collected
        loaded_locations.append({"provider":"visualcrossing"}|json)
        msg(id,json["resolvedAddress"])
        day=0
        msg(id,"СЕГОДНЯ:\nТемпература: {temp}\nВлажность: {humidity}%\nСкорость ветра: {ws} км в час\nНаправление ветра: {wd}\nПогода: {conditions}\n{desc}".format(
            temp=f"{json["days"][day]["tempmin"]}°C-{json["days"][day]["tempmax"]}°C",humidity=json["days"][day]["humidity"],conditions=json["days"][day]["conditions"],desc=json["days"][day]["description"],ws=json["days"][day]["windspeed"],wd=windir(json["days"][day]["winddir"])))

        day=1
        msg(id,"ЗАВТРА:\nТемпература: {temp}\nВлажность: {humidity}%\nСкорость ветра: {ws} км в час\nНаправление ветра: {wd}\nПогода: {conditions}\n{desc}".format(
            temp=f"{json["days"][day]["tempmin"]}°C-{json["days"][day]["tempmax"]}°C",humidity=json["days"][day]["humidity"],conditions=json["days"][day]["conditions"],desc=json["days"][day]["description"],ws=json["days"][day]["windspeed"],wd=windir(json["days"][day]["winddir"])))
        
        msg(id,"СЕЙЧАС:\nТемпература: {temp}\nВлажность: {humidity}%\nСкорость ветра: {ws} км в час\nНаправление ветра: {wd}\nВот такие пироги!".format(
            temp=f"{json["currentConditions"]["temp"]}°C",humidity=json["currentConditions"]["humidity"],ws=json["currentConditions"]["windspeed"],wd=windir(json["currentConditions"]["winddir"])))


@bot.message_handler(commands=["weatherpos"])
def getpos(m):
    id=m.from_user.id
    if id in loaded_users:
        add_chat(m)
        try:
            array=m.text.split(" ")
            if len(array)!=3:raise Exception("Передано 0 или более 2 элементов")
            if not -90<=float(array[1])<=90: Exception("Число широты вне диапозона -90 и 90")
            if not -180<=float(array[2])<=180: Exception("Число долготы вне диапозона -180 и 180")
            LocationByLatLon(id,float(array[1]),float(array[2]))
        except (TypeError,ValueError):
            msg(id,"✋🤨 Неправильный формат (Широта и/или долгота не являются числами)")
        except Exception as e:
            msg(id,f"✋🤨 Неправильный формат ({e})")

@bot.message_handler(commands=["weathername"])
def getname(m):
    id=m.from_user.id
    if id in loaded_users:
        add_chat(m)
        try:
            array=m.text.split(" ")
            if len(array)!=2:raise Exception("Передано 0 или более 1 элемента")
            if len(array[1])<5:raise Exception("Название места меньше 5 символов")
            LocationByName(id,array[1])
        except Exception as e:
            msg(id,f"✋🤨 Неправильный формат ({e})")

@bot.message_handler(commands=["weatherzip"])
def getzip(m):
    id=m.from_user.id
    if id in loaded_users:
        add_chat(m)
        try:
            array=m.text.split(" ")
            if len(array)!=2:raise Exception("Передано 0 или более 1 элемента")
            if len(array[1])!=5: raise Exception("Неверный американский почтовый индекс")
            LocationByName(id,array[1])
        except Exception as e:
            msg(id,f"✋🤨 Неправильный формат ({e})")
@bot.message_handler(content_types=["location"])
def handle_location(message):
    if message.from_user.id in loaded_users and message.location is not None:
        cid=message.chat.id
        lat = message.location.latitude
        lon = message.location.longitude
        msg(cid, f"🤩 Мы получили ваши координаты!\nШирота: <tg-spoiler>({lat})</tg-spoiler>\nДолгота: <tg-spoiler>({lon})</tg-spoiler>",parse_mode='HTML')
        LocationByLatLon(cid,lat,lon)
            



@bot.message_handler(content_types=["text"])
def textChecker(message):
    if message.from_user.id in loaded_users:
        add_chat(message)
         # Обработчик админ-отправки сообщений
        if check_admin(message) and currently_in_admin[message.from_user.id]=="shogochit":
            currently_in_admin[message.from_user.id]="idle"
            for chat in loaded_chats:
                msg(chat,message.text)
            msg(message.chat.id,"🚀 Сообщение отправлено всем юзерам бота!",reply_markup=adminKeyboard)










print("инициализирован!")
bot.infinity_polling()
print("Остановились!")
JSON_save()