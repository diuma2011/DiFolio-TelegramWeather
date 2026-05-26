from requests import get
from re import match
badreq=r"Bad API Request".lower()

class VCWAPIError(Exception):
    """
    Общая ошибка, когда при запросе Visual Crossing Weather API происходит какие-то проблемы

    Тест 100 - Спровоцировать ошибку "Локация не найдена"
    >>> try: get_data_with_name("Оребаш")
    ... except VCWAPIError as e:
    ...     print(e[:8])
    CODE 400

    Тест 101 - Поймать любую ошибку, связанную с VCWAPIError
    >>> try: get_data_with_name("...")
    ... except VCWAPIError:
    ...     print("Пережили!")
    Пережили!
    """

class BadRequest400(VCWAPIError):
    """
    Общая ошибка, когда происходит ошибка 400

    Тест 102 - Поймать любую ошибку, связанную с BadRequest400
    >>> try: get_data_with_pos(12,34,"next1Day")
    ... except BadRequest400 as e:
    ...     print(e)
    CODE 400 – Неправильный формат старта времени. Формат времени должно соответствовать yyyy-M-d['T'H:m:s][.SSS][X]
    
    Тест 103 - Поймать ошибку, связанную с BadRequest и исправить его
    >>> lat,lon=96,96
    >>> while True:
    ...     try:
    ...         data=get_data_with_pos(lat,lon)
    ...     except BadRequest400:
    ...         lat-=5
    ...         lon-=5
    ...     else:
    ...         print(data["address"])
    ...         break
    86,86
    """

class InvalidLocation(BadRequest400):
    """
    Общая ошибка, когда локация некорректна
    
    Тест 104 - Получить заготовленные данные с массива и написать о количестве корректных и некорректных мест
    >>> locations=["12.23,","London","Barnaul","...","*!@#%^&*())"]
    >>> sum,unsum=0,0
    >>> for l in locations:
    ...     try:
    ...         get_data_with_name(l)
    ...         sum+=1
    ...     except InvalidLocation:
    ...         unsum+=1
    ... print(sum,unsum)
    2 3
    """

class TooShortLocation(InvalidLocation):
    """
    Локация слишком короткая, чтобы его определить
    
    Тест 105 - Без получения локации сразу определить, какие строки меньше длины в 5 символов
    >>> locations=["Амзя","Хагасаки","Мишкино","Египет","Рим"]
    >>> # если че, каждая из локаций существует лол :D
    >>> unsupport=[]
    >>> for l in locations:
    ...     try:
    ...         if len(l)<5: raise TooShortLocation
    ...     except TooShortLocatiob:
    ...         unsupport.append(l)
    ... print(*unsupport)
    Амзя Рим
    """
class LocationNoFound(InvalidLocation):
    """
    Локация не найдена
    
    Тест 106 - Найти локацию "Ромашковая долина смешарики"
    >>> try:data=get_data_with_name("Ромашковая долина смешарики")
    ... except LocationNoFound: print("Не найдено(")
    Не найдено(
    """
class NoLocation(InvalidLocation):
    """
    Локация не введена
    
    Тест 107 - Начать поэтапно делать запрос каждой локации, до пустой локации
    >>> locations=["П","Щекур","Мадагаскар","Пирамида Хеопса","Чернобыль","","Москва"]
    >>> cycle=0
    >>> for l in locations:
    ...     cycle+=1
    ...     try:
    ...         get_data_with_name(l)
    ...     except NoLocation:
    ...         print("ОСТАНОВКА",cycle)
    ...     except InvalidLocation:
    ...         cycle=0
    ОСТАНОВКА 5
    """
class InvalidLocationFormat(InvalidLocation):
    """Локация не является текстовым местом, lan и lon числами или US ZIP индексом"""
class InvalidLocationExpression(InvalidLocation):
    """Локация состоит только из спец символов"""
class InvalidZipCode(InvalidLocation):
    """Почтовый индекс Америки не найден"""

class IncorrectDate(BadRequest400):
    """Общая ошибка, когда введена некорректная дата/время"""

class IncorrectDateFormat(IncorrectDate):
    """Некорректное время"""
class UnboundYear(IncorrectDate):
    """Указанный год за пределами 1950 и 2050"""
class Date2Before1(IncorrectDate):
    """Временной промежуток вывернут наизнанку (Конечная точка раньше стартовой точки)"""
class DateUnderLimit(IncorrectDate):
    """Время раньше 1970-01-01 00:00:00Z"""

class TooLongURL(BadRequest400):
    """Ссылка слишком длинная"""

class InvalidAPIKey(VCWAPIError):
    """Неверный API ключ"""
class NoAPIKey(VCWAPIError):
    """Пустой API ключ"""

class DailyLimit(VCWAPIError):
    """Лимит дня превышен"""

class IncorrectEndpoint(VCWAPIError):
    """Конечный Endpoint не соответствуется"""

class InternalServerError(VCWAPIError):
    pass
API_KEY="балбес"
with open("VCWAPIKEY.txt","r") as f:
    API_KEY=f.read()
URL="https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
ATTRIBUTS={
    "key":API_KEY,
    "unitGroup":"metric",
    "lang":"ru",
    "contentType":"json"
}

def get_data_with_name(pos,*endpoints,**params):
    """
    Получение данных о погоде с названия места

    Тест 000: Успешное чтение координат 0,0 и получение введённого адреса
    >>> json=get_data_with_pos(0,0)
    >>> print(json["address"])
    0,0

    Тест 001: Успешный поиск города Москвы и получение временного пояса
    >>> json=get_data_with_name("Москва")
    >>> print(json["timezone"])
    Europe/Moscow

    Тест 002: Поиск по "Калмаш,Калтасинский район" и получение временного пояса
    >>> json=get_data_with_name("Калмаш,Калтасинский район")
    >>> print(json["timezone"])
    Asia/Yekaterinburg

    Тест 003: Поиск по почтовому индексу Америки 10001 (Нью-Йорк) и получение округлённую позицию
    >>> json=get_data_with_name("10001")
    >>> print(json["latitude"][:2])
    40

    Тест 004: Получить погоду на 24 часа и получить кол-во записей часов
    >>> json=get_data_with_name("Лондон","next24hours")
    >>> print(len(json["days"]),len(json["days"]["hours"]))
    2 24
    """
    ENDPOINTS=[]
    ENDPOINTS.append(pos)
    ENDPOINTS.extend(endpoints)
    url=get(URL+"/".join(ENDPOINTS),params=ATTRIBUTS|params,headers={
    "User-Agent":r"Telegram Project for Uchi.Doma @dimkainsprojects_tgproject_bot (contact diuma.dog@gmail.com)",
    'From': 'Dimkain'
    })
    # print(url.url)
    error_handler(url.text,url.status_code,0)
    return url.json()
def get_data_with_pos(lat,lon,*endpoints,**params):

    ENDPOINTS=[]
    ENDPOINTS.append(f"{lat},{lon}")
    ENDPOINTS.extend(endpoints)
    url=get(URL+"/".join(ENDPOINTS),params=ATTRIBUTS|params,headers={
    "User-Agent":r"Telegram Project for Uchi.Doma @dimkainsprojects_tgproject_bot (contact diuma.dog@gmail.com)",
    'From': 'Dimkain'
    })
    # print(url.url)
    error_handler(url.text,url.status_code,0)
    return url.json()

def error_simplimator(status,TEXT):
    return f"CODE {status} – {TEXT}"
def error_handler(text,status,operation):
    """
    Отсеивает возможные ошибки

    Тест 005: Получить
    >>> try:
    ...     json=get_data_with_pos(666,444,"next24hours")
    ...     print(json["address"])
    ... except LocationNoFound:
    ...     print("Локация не найдена!")
    Локация не найдена!
    >>> try:
    ...     json=get_data_with_name("a","next24hours")
    ...     print(json["address"])
    ... except TooShortLocation:
    ...     print("Очень коротко")
    Очень коротко
    >>> try:
    ...     json=get_data_with_name("")
    ...     print(json["address"])
    ... except NoLocation:
    ...     print("Без локации")
    Без локации
    >>> try:
    ...     json=get_data_with_name("ooo"*1024,"next24hours")
    ...     print(json["address"])
    ... except TooLongURL:
    ...     print("Длинная ссылка!")
    Длинная ссылка!
    >>> try:
    ...     json=get_data_with_name("оыфор%:?*?:;*:?%*?;фЫВ;;:;;;;;;:%:?:?*?*?")
    ...     print(json["address"])
    ... except VCWAPIError:
    ...     print("Ошибка!")
    Ошибка!
    >>> try:
    ...     json=get_data_with_name("гойда")
    ...     print(json["address"])
    ... except VCWAPIError:
    ...     print("Ошибка!")
    Ошибка!
    """
    text=text.lower()
    if match(badreq,text) or status==400:
        razdel=text.split(":")[1]
        if match("Address is too short to be uniquely identified".lower(),razdel):
            raise TooShortLocation(error_simplimator(status,"Указанная локация слишком короткая для его поиска (длина менее 5 букв)"))
        if match("No valid locations could be determined from the input".lower(),razdel):
            raise LocationNoFound(error_simplimator(status,"Локация не найдена. Возможно, у вас опечатка."))
        if match("A location must be specified".lower(),razdel):
            raise NoLocation(error_simplimator(status,"Поле локации пустое."))
        if match(r"Start date time value .* cannot be parsed".lower(),razdel):
            raise IncorrectDateFormat(error_simplimator(status,"Неправильный формат старта времени. Формат времени должно соответствовать yyyy-M-d['T'H:m:s][.SSS][X]"))
        if match("Start date cannot be before 1970-01-01 00:00:00Z".lower(),razdel):
            raise DateUnderLimit(error_simplimator(status,"Указано время, уходящий за минимальный лимит 1970-01-01 00:00:00Z"))
        if match(r"Invalid year requested\. Years must be between 1950 and 2050".lower(),razdel):
            raise UnboundYear(error_simplimator(status,"Указанный год не входит в пределы 1950-2050"))
        if match(r"To date \(.*\) cannot be before the from date \(.*\)".lower(),razdel):
            raise Date2Before1(error_simplimator(status,"Конечное время не может быть ранее стартового времени"))
        if match("Address is too long".lower(),razdel):
            raise TooLongURL(error_simplimator(status,"Полученная ссылка слишком длинная"))
        if match("Invalid address format".lower(), razdel):
            raise InvalidLocationFormat(error_simplimator(status, "Некоретный формат адреса (Текст локации не строковое, не является lan,lon или US почтовым индексом из 5 цифр)"))
        if match("Invalid address characters found".lower(),razdel):
            raise InvalidLocationExpression(error_simplimator(status, "Локация состоит из спец. символов"))
        if match("Could not find zip code",razdel):
            raise InvalidZipCode(error_simplimator(status,"Почтовый индекс Америки не найден"))
        raise BadRequest400(error_simplimator(status,text))
    if match("No account found with API key".lower(),text):
        raise InvalidAPIKey(error_simplimator(status,"Неправильный или нерабочий API ключ."))
    if match("No session or key found".lower(),text):
        raise NoAPIKey(error_simplimator(status,"Поле API ключа пустое."))
    if match("Request did not match an endpoint".lower(),text):
        raise IncorrectEndpoint(error_simplimator(status,"Конечный endpoint не соответствует ожиданному."))
    if match("Maximum daily cost exceeded".lower(),text) or status==429:
        raise DailyLimit(error_simplimator(status,"Ежедневный лимит запросов превышен"))
    if status==500:
        raise InternalServerError(error_simplimator(status,"Ошибка сервера."))
    if status!=200:
        raise VCWAPIError(error_simplimator(status,text))

# dataTest=get_data_with_pos(12,-34,"next24hours")
# # dataTest=get_data_with_pos(999,999,"next24hours")
# days=dataTest["days"]
# print("days:",len(days))
# # print(days)
# today=days[0]
# tommorow=days[1]
# print("СЕГОДНЯ:\nТемпература: {temp}°C\nВлажность: {humidity}%\nПогода: {conditions}\n{desc}".format(
#     temp=today["temp"],humidity=today["humidity"],conditions=today["conditions"],desc=today["description"]))
# print("ЗАВТРА:\nТемпература: {temp}°C\nВлажность: {humidity}%\nПогода: {conditions}\n{desc}".format(
#     temp=tommorow["temp"],humidity=tommorow["humidity"],conditions=tommorow["conditions"],desc=tommorow["description"]))