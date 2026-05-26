from typing import overload, Union, List, Optional

from requests import get
API_KEY="балбес"
with open("VCWAPIKEY.txt","r") as f:
    API_KEY=f.read()
URL="https://api.open-meteo.com/v1/forecast"
# ATTRIBUTS={
#     "temperature_unit":"celcius",
# }

WEATHER_CODES = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Ледяной туман с изморозью",
    51: "Слабая морось",
    53: "Умеренная морось",
    55: "Плотная морось",
    56: "Слабая замерзающая морось",
    57: "Плотная замерзающая морось",
    61: "Слабый дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    66: "Слабый замерзающий дождь",
    67: "Сильный замерзающий дождь",
    71: "Слабый снегопад",
    73: "Умеренный снегопад",
    75: "Сильный снегопад",
    77: "Снежные зерна (крупа)",
    80: "Слабый ливневый дождь",
    81: "Умеренный ливневый дождь",
    82: "Сильный, сильный ливневый дождь",
    85: "Слабый ливневый снегопад",
    86: "Сильный ливневый снегопад",
    95: "Гроза (слабая или умеренная)",
    96: "Гроза со слабым градом",
    99: "Гроза с сильным градом"}
WIND_DIRS={
    0:"Северный",
    1:"Северо-Восточный",
    2:"Восточный",
    3:"Юго-Восточный",
    4:"Южный",
    5:"Юго-Западный",
    6:"Западный",
    7:"Северо-западный",
}
def windir(dir:int|float):
    cod=0
    if 337.5<dir or dir<=22.5:cod=0
    elif 22.5<dir<=67.5: cod=1
    elif 67.5<dir<=112.5: cod=2
    elif 112.5<dir<=157.5: cod=3
    elif 157.5<dir<=202.5:cod=4
    elif 202.5<dir<=247.5: cod=5
    elif 247.5<dir<=292.5: cod=6
    elif 292.5<dir<=337.5: cod=7
    return WIND_DIRS[cod]



class OpenMeteoCollectedData():
    @overload
    def __init__(self,
    latitude:float|int, longitude:float|int,
    elevation=None, 
    hourly=None, daily=None, current=None, 
    temperature_unit=None, wind_speed_unit=None, precipitation_unit=None, 
    timeformat=None, timezone=None,
    past_days=None, forecast_days=None,
    forecast_hours=None, forecast_minutely_15=None,
    past_hours=None,past_minutely_15=None,
    start_date=None,end_date=None,
    start_hour=None,end_hour=None,
    start_minutely_15=None,end_minutely_15=None,
    models=None,cell_selection=None,apikey=None):
        pass
    @overload
    def __init__(self, latitude:str, longitude:str,
    elevation=None, 
    hourly=None, daily=None, current=None, 
    temperature_unit=None, wind_speed_unit=None, precipitation_unit=None, 
    timeformat=None, timezone=None,
    past_days=None, forecast_days=None,
    forecast_hours=None, forecast_minutely_15=None,
    past_hours=None,past_minutely_15=None,
    start_date=None,end_date=None,
    start_hour=None,end_hour=None,
    start_minutely_15=None,end_minutely_15=None,
    models=None,cell_selection=None,apikey=None):
        pass

    def __init__(self,latitude:Union[float, str],longitude:Union[float, str],
    elevation=None, 
    hourly=None, daily=None, current=None, 
    temperature_unit=None, wind_speed_unit=None, precipitation_unit=None, 
    timeformat=None, timezone=None,
    past_days=None, forecast_days=None,
    forecast_hours=None, forecast_minutely_15=None,
    past_hours=None,past_minutely_15=None,
    start_date=None,end_date=None,
    start_hour=None,end_hour=None,
    start_minutely_15=None,end_minutely_15=None,
    models=None,cell_selection=None,apikey=None):
        data=get_data_with_pos(latitude,longitude,
    elevation=elevation, 
    hourly=hourly, daily=daily, current=current, 
    temperature_unit=temperature_unit, wind_speed_unit=wind_speed_unit, precipitation_unit=precipitation_unit, 
    timeformat=timeformat, timezone=timezone,
    past_days=past_days, forecast_days=forecast_days,
    forecast_hours=forecast_hours, forecast_minutely_15=forecast_minutely_15,
    past_hours=past_hours, past_minutely_15=past_minutely_15,
    start_date=start_date, end_date=end_date,
    start_hour=start_hour, end_hour=end_hour,
    start_minutely_15=start_minutely_15, end_minutely_15=end_minutely_15,
    models=models, cell_selection=cell_selection, apikey=apikey)
        self.json=data
    #     get(URL,{
    # "latitude":latitude,"longitude":longitude,
    # "elevation":elevation, 
    # "hourly":hourly, "daily":daily, "current":current, 
    # "temperature_unit":temperature_unit, "wind_speed_unit":wind_speed_unit, "precipitation_unit":precipitation_unit, 
    # "timeformat":timeformat, "timezone":timezone,
    # "past_days":past_days, "forecast_days":forecast_days,
    # "forecast_hours":forecast_hours, "forecast_minutely_15":forecast_minutely_15,
    # "past_hours":past_hours,"past_minutely_15":past_minutely_15,
    # "start_date":start_date,"end_date":end_date,
    # "start_hour":start_hour,"end_hour":end_hour,
    # "start_minutely_15":start_minutely_15,"end_minutely_15":end_minutely_15,
    # "models":models,"cell_selection":cell_selection,"apikey":apikey})

def get_data_with_pos(lat,lon,**attributes):
    url=get(URL,params={"latitude":lat,"longitude":lon}|attributes,headers={
    "User-Agent":r"Telegram Project for Uchi.Doma @dimkainsprojects_tgproject_bot (contact diuma.dog@gmail.com)",
    'From': 'Dimkain'
    })
    return url.json()
# OpenMeteoCollectedData(12.23,67.67)
# dataTest=get_data_with_pos(30,-60)
# days=dataTest["days"]
# print("days:",len(days))
# # print(days)
# today=days[0]
# tommorow=days[1]
# print("СЕГОДНЯ:\nТемпература: {temp}°C\nВлажность: {humidity}%\nПогода: {conditions}\n{desc}".format(
#     temp=today["temp"],humidity=today["humidity"],conditions=today["conditions"],desc=today["description"]))
# json=get("https://api.open-meteo.com/v1/forecast?latitude=56.059626&longitude=54.610471&daily=weather_code,temperature_2m_max,temperature_2m_min&current=temperature_2m,rain,showers,snowfall,is_day,wind_speed_10m,wind_direction_10m&timezone=auto&forecast_days=2").json()


# json=OpenMeteoCollectedData(56.059626,54.610471,daily="weather_code,temperature_2m_max,temperature_2m_min",current="temperature_2m,relative_humidity_2m,weather_code",timezone="auto",forecast_days=2)
# print(json)
# print(json.json)

# day=0

# print("СЕГОДНЯ:\nТемпература: {temp}\nВлажность: {humidity}\nПогода: {conditions}\n{desc}".format(
#     temp=f"{json.json["daily"]["temperature_2m_min"][day]}°C-{json.json["daily"]["temperature_2m_max"][day]}°C",humidity="Нету",conditions=WEATHER_CODES[json.json["daily"]["weather_code"][day]],desc="Вот такие пироги!"))

# day=1

# print("Завтра:\nТемпература: {temp}\nВлажность: {humidity}\nПогода: {conditions}\n{desc}".format(
#     temp=f"{json.json["daily"]["temperature_2m_min"][day]}°C-{json.json["daily"]["temperature_2m_max"][day]}°C",humidity="Нету",conditions=WEATHER_CODES[json.json["daily"]["weather_code"][day]],desc="Вот такие пироги!"))

# print("СЕЙЧАС:\nТемпература: {temp}\nВлажность: {humidity}\nПогода: {conditions}\n{desc}".format(
#     temp=f"{json.json["current"]["temperature_2m"]}°C",humidity=str(json.json["current"]["relative_humidity_2m"])+"%",conditions=WEATHER_CODES[json.json["current"]["weather_code"]],desc="Вот такие пироги!"))