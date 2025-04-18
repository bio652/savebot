from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import channels

async def channelkbbuilder():
    builder = InlineKeyboardBuilder()
    for key, val in channels.items():
        builder.add(InlineKeyboardButton(text="✔Подпишись на канал✔", url=val))
    builder.add(InlineKeyboardButton(text="✅Проверить✅", callback_data="check"))
    return builder.as_markup()

adminMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить канал', callback_data="addchannel")],
    [InlineKeyboardButton(text='Убрать канал', callback_data="delchannel")]
])

adminbackMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data="adminback")]
])