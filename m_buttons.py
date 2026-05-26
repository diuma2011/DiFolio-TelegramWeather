from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
preKeyboard=ReplyKeyboardMarkup(True)
preKeyboard.add("Подтверждаю")
preKeyboard.add("Что собирает приложение")

# keyboard=ReplyKeyboardMarkup(True,True)
# keyboard.add(KeyboardButton("Котика!"))
# keyboard.add(KeyboardButton("Гиф-Котика!"))

menuKeyboard=ReplyKeyboardMarkup(True,True)
menuKeyboard.add(KeyboardButton("Отправить геолокацию",request_location=True))
menuKeyboard.add(KeyboardButton("Текущая погода в разных местах"))
menuKeyboard.add(KeyboardButton("Статистика"))
menuKeyboard.add(KeyboardButton("О проекте"))
menuKeyboard.add(KeyboardButton("Помощь"))

adminKeyboard=ReplyKeyboardMarkup(True)
adminKeyboard.add(KeyboardButton("Остановка бота"))
adminKeyboard.add(KeyboardButton("Сообщение всем"))
adminKeyboard.add(KeyboardButton("JSON меню"))
adminKeyboard.add(KeyboardButton("Закрыть админ сессию"))

adminKeyboardMessage=ReplyKeyboardMarkup(True)
adminKeyboardMessage.add(KeyboardButton("/stop"))

adminKeyboardJSON=ReplyKeyboardMarkup(True)
adminKeyboardJSON.add(KeyboardButton("Обновить датабазу JSON"))
adminKeyboardJSON.add(KeyboardButton("Назад"))