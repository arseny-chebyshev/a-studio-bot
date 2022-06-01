from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ADD TEXT CMD')],
    [KeyboardButton(text='CANCEL')]
],  resize_keyboard=True, one_time_keyboard=True)

request_phone_button_kbd = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🖊 Записаться", request_contact=True), KeyboardButton(text="❌ Отмена")],
], resize_keyboard=True)

