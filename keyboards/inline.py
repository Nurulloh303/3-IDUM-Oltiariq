from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def classes_inline_keyboard(classes):
    markup = InlineKeyboardMarkup()
    for cls in classes:
        markup.add(InlineKeyboardButton(text=cls, callback_data=f"class_{cls}"))
    return markup

def weekdays_inline_keyboard():
    days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"]
    markup = InlineKeyboardMarkup()
    for day in days:
        markup.add(InlineKeyboardButton(text=day, callback_data=f"day_{day}"))
    return markup
