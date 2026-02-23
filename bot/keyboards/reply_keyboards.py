from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Convert Currency"), KeyboardButton("Help"))
    markup.add(KeyboardButton("Sweet Message"), KeyboardButton("Instagram Downloader"))
    return markup

def get_cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("❌ Cancel"))
    return markup

def get_currency_direction_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("USD ⮕ KRW"), KeyboardButton("KRW ⮕ USD"))
    markup.add(KeyboardButton("❌ Cancel"))
    return markup
