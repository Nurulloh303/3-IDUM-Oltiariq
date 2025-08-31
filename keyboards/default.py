from telebot import types

# === FOYDALANUVCHI MENYU ===
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("📚 Dars jadvali"))
    return kb

# === ADMIN MENYU ===
def admin_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("🏫 Sinflar"))
    kb.add(types.KeyboardButton("📅 Dars jadvali"))
    return kb

# === FOYDALANUVCHI TELEFON SO‘RASH TUGMASI ===
def phone_request_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True))
    return kb
