from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def CreateReply(args) -> ReplyKeyboardBuilder:
    bulder = ReplyKeyboardBuilder()
    for i in args:
        bulder.add(KeyboardButton(text=i.text))
    bulder.adjust(2)
    return bulder.as_markup(resize_keyboard=True,one_time_keyboard=True)
