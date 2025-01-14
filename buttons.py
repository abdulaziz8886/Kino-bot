from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
kanal = {
    "1-Kanal" : "https://t.me/khayrullayev121",
    '2-Kanal' : 'https://t.me/kinolar_azik'
}



tugma = InlineKeyboardBuilder()
for i in kanal:
    tugma.button(text=f"{i}", url=f"{kanal[f'{i}']}")
tugma.button(text = "Tekshirish ✅", callback_data="tekshir")
tugma.adjust(1)


buttom_admin = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text='Kino qoshish'), KeyboardButton(text='Kino o\'chirish')]
    ], one_time_keyboard=True, resize_keyboard=True
)



Buttom_tekshir = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ha 👍", callback_data="ha"), InlineKeyboardButton(text="Yoq 👎",callback_data="yoq")]
    ]
)