from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def CreateInline(args) -> InlineKeyboardBuilder:
    bulder = InlineKeyboardBuilder()
    for i in args:
        bulder.add(InlineKeyboardButton(text=i.text, callback_data=i.callback_data))
    bulder.adjust(2)
    return bulder.as_markup()

def sub_check(channels):
    keyboard = InlineKeyboardBuilder()
    for name, url in channels:
        keyboard.add(InlineKeyboardButton(text=f'Подписаться на {name}', url=url))
    keyboard.add(InlineKeyboardButton(text='Я подписался', callback_data='chanel_sub'))
    keyboard.adjust(1)
    return keyboard.as_markup()