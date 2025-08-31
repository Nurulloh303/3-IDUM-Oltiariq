from telebot import types
from database.db import db
from keyboards.default import main_menu, phone_request_kb
from config import ADMINS

def register_user_handlers(bot):

    @bot.message_handler(commands=['start'])
    def user_start(message):
        if message.chat.id in ADMINS:
            return  # admin start handleri ishlaydi, foydalanuvchi o'tmaydi

        user = db.get_user(message.chat.id)
        if not user:
            msg = bot.send_message(
                message.chat.id,
                "📱 Ro‘yxatdan o‘tish uchun telefon raqamingizni yuboring:",
                reply_markup=phone_request_kb()
            )
            bot.register_next_step_handler(msg, get_phone)
        else:
            bot.send_message(message.chat.id, "👋 Xush kelibsiz!", reply_markup=main_menu())

    def get_phone(message):
        if not message.contact:
            msg = bot.send_message(
                message.chat.id,
                "❌ Iltimos, tugma orqali telefon raqamingizni yuboring.",
                reply_markup=phone_request_kb()
            )
            bot.register_next_step_handler(msg, get_phone)
            return
        phone = message.contact.phone_number
        db.add_user(message.chat.id, None, phone)
        msg = bot.send_message(
            message.chat.id,
            "👤 Ism va familiyangizni kiriting (masalan: Ali Valiyev):",
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(msg, get_name)

    def get_name(message):
        full_name = message.text.strip()
        db.update_user_name(message.chat.id, full_name)
        classes = db.get_classes()
        if not classes:
            bot.send_message(message.chat.id, "❌ Hozircha sinflar qo‘shilmagan.")
            return
        kb = types.InlineKeyboardMarkup()
        for c in classes:
            kb.add(types.InlineKeyboardButton(text=c[1], callback_data=f"setclass_{c[0]}"))
        bot.send_message(message.chat.id, "🏫 Sinfingizni tanlang:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("setclass_"))
    def set_class(call):
        class_id = call.data.split("_")[1]
        db.update_user_class(call.message.chat.id, class_id)
        bot.edit_message_text(
            "✅ Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(call.message.chat.id, "📌 Endi menyudan foydalanishingiz mumkin.", reply_markup=main_menu())

    @bot.message_handler(func=lambda m: m.text == "📚 Dars jadvali")
    def show_schedule(message):
        user = db.get_user(message.chat.id)
        if not user or not user[3]:
            bot.send_message(message.chat.id, "❌ Avval ro‘yxatdan o‘ting va sinfni tanlang.")
            return
        days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"]
        kb = types.InlineKeyboardMarkup()
        for d in days:
            kb.add(types.InlineKeyboardButton(text=d, callback_data=f"day_{d}_{user[3]}"))
        bot.send_message(message.chat.id, "📅 Haftaning kunini tanlang:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
    def show_day_schedule(call):
        _, day, class_id = call.data.split("_")
        lessons = db.get_schedule(class_id, day)
        if not lessons:
            text = f"❌ {day} kuni uchun dars jadvali yo‘q."
        else:
            text = f"📅 {day} dars jadvali:\n\n"
            for idx, l in enumerate(lessons, start=1):
                text += f"{idx}. {l}\n"
        bot.send_message(call.message.chat.id, text)
