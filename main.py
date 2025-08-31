from telebot import TeleBot
from config import TOKEN, ADMINS
from handlers.admin import  admin_handlers
from handlers.users import user_handlers
# === BOTNI YARATISH ===
bot = TeleBot(TOKEN)

# === HANDLERLARNI RO'YXATDAN O‘TKAZISH ===
admin_handlers.register_admin_handlers(bot, ADMINS)  # Admin handlerlari

user_handlers.register_user_handlers(bot)       # Foydalanuvchi handlerlari

# === BOTNI ISHGA TUSHIRISH ===
bot.infinity_polling()
