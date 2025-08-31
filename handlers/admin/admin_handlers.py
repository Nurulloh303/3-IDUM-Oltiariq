from telebot import types
from database.db import db
from keyboards.default import admin_menu
from config import ADMINS

def register_admin_handlers(bot, ADMINS):

    # === ADMIN START ===
    @bot.message_handler(commands=['admin'])
    def admin_start(message):
        if message.chat.id not in ADMINS:
            return
        bot.send_message(message.chat.id, "👮‍♂️ Admin panel", reply_markup=admin_menu())

    # === SINFLAR ===
    @bot.message_handler(func=lambda m: m.text == "🏫 Sinflar")
    def manage_classes(message):
        if message.chat.id not in ADMINS:
            return
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("➕ Qo‘shish", callback_data="class_add"))
        kb.add(types.InlineKeyboardButton("🗑 O‘chirish", callback_data="class_delete"))
        kb.add(types.InlineKeyboardButton("✏️ O‘zgartirish", callback_data="class_edit"))
        bot.send_message(message.chat.id, "🏫 Sinflar bo‘limi:", reply_markup=kb)

    # --- ADD CLASS ---
    @bot.callback_query_handler(func=lambda call: call.data == "class_add")
    def add_class_start(call):
        if call.message.chat.id not in ADMINS: return
        msg = bot.send_message(call.message.chat.id, "✏️ Yangi sinf nomini kiriting:")
        bot.register_next_step_handler(msg, add_class_finish)

    def add_class_finish(message):
        db.add_class(message.text.strip())
        bot.send_message(message.chat.id, "✅ Sinf qo‘shildi.")

    # --- DELETE CLASS ---
    @bot.callback_query_handler(func=lambda call: call.data == "class_delete")
    def delete_class_start(call):
        if call.message.chat.id not in ADMINS: return
        classes = db.get_classes()
        if not classes:
            bot.send_message(call.message.chat.id, "❌ Hali sinflar yo‘q.")
            return
        kb = types.InlineKeyboardMarkup()
        for c in classes:
            kb.add(types.InlineKeyboardButton(text=c[1], callback_data=f"classdel_{c[0]}"))
        bot.send_message(call.message.chat.id, "🗑 O‘chirish uchun sinfni tanlang:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("classdel_"))
    def delete_class_finish(call):
        if call.message.chat.id not in ADMINS: return
        class_id = call.data.split("_")[1]
        db.delete_class(class_id)
        bot.edit_message_text("✅ Sinf o‘chirildi.",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)

    # --- EDIT CLASS ---
    @bot.callback_query_handler(func=lambda call: call.data == "class_edit")
    def edit_class_start(call):
        if call.message.chat.id not in ADMINS: return
        classes = db.get_classes()
        if not classes:
            bot.send_message(call.message.chat.id, "❌ Hali sinflar yo‘q.")
            return
        kb = types.InlineKeyboardMarkup()
        for c in classes:
            kb.add(types.InlineKeyboardButton(text=c[1], callback_data=f"classedit_{c[0]}"))
        bot.send_message(call.message.chat.id, "✏️ O‘zgartirish uchun sinfni tanlang:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("classedit_"))
    def edit_class_name(call):
        if call.message.chat.id not in ADMINS: return
        class_id = call.data.split("_")[1]
        msg = bot.send_message(call.message.chat.id, "✏️ Yangi nomni kiriting:")
        bot.register_next_step_handler(msg, lambda m: edit_class_finish(m, class_id))

    def edit_class_finish(message, class_id):
        db.update_class(class_id, message.text.strip())
        bot.send_message(message.chat.id, "✅ Sinf nomi yangilandi.")

    # === DARS JADVALI ===
    @bot.message_handler(func=lambda m: m.text == "📅 Dars jadvali")
    def manage_schedule(message):
        if message.chat.id not in ADMINS: return
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("➕ Qo‘shish", callback_data="lesson_add"))
        kb.add(types.InlineKeyboardButton("🗑 O‘chirish", callback_data="lesson_delete"))
        kb.add(types.InlineKeyboardButton("✏️ O‘zgartirish", callback_data="lesson_edit"))
        bot.send_message(message.chat.id, "📚 Dars jadvali bo‘limi:", reply_markup=kb)

    # --- ADD LESSON ---
    @bot.callback_query_handler(func=lambda call: call.data.startswith("lesson_add"))
    def add_lesson_start(call):
        if call.message.chat.id not in ADMINS: return
        classes = db.get_classes()
        if not classes:
            bot.send_message(call.message.chat.id, "❌ Hali sinflar yo‘q.")
            return
        kb = types.InlineKeyboardMarkup()
        for c in classes:
            kb.add(types.InlineKeyboardButton(text=c[1], callback_data=f"lessonadd_{c[0]}"))
        bot.send_message(call.message.chat.id, "📌 Qaysi sinf uchun dars qo‘shmoqchisiz?", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("lessonadd_"))
    def add_lesson_day(call):
        if call.message.chat.id not in ADMINS: return
        class_id = call.data.split("_")[1]
        kb = types.InlineKeyboardMarkup()
        days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"]
        for d in days:
            kb.add(types.InlineKeyboardButton(text=d, callback_data=f"lessonaddday_{class_id}_{d}"))
        bot.send_message(call.message.chat.id, "📅 Haftaning kunini tanlang:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("lessonaddday_"))
    def add_lesson_finish(call):
        if call.message.chat.id not in ADMINS: return
        _, class_id, day = call.data.split("_")
        msg = bot.send_message(call.message.chat.id, f"✏️ {day} kuni uchun darslarni yozing (vergul bilan ajrating):")
        bot.register_next_step_handler(msg, lambda m: save_lesson(m, class_id, day))

    def save_lesson(message, class_id, day):
        lessons = [l.strip() for l in message.text.strip().split(",")]
        db.add_schedule(class_id, day, lessons)
        bot.send_message(message.chat.id, "✅ Dars jadvali qo‘shildi.")

    # --- DELETE LESSON ---
    @bot.callback_query_handler(func=lambda call: call.data.startswith("lesson_delete"))
    def delete_lesson_start(call):
        if call.message.chat.id not in ADMINS: return
        classes = db.get_classes()
        if not classes:
            bot.send_message(call.message.chat.id, "❌ Hali sinflar yo‘q.")
            return
        kb = types.InlineKeyboardMarkup()
        for c in classes:
            kb.add(types.InlineKeyboardButton(text=c[1], callback_data=f"lessondel_{c[0]}"))
        bot.send_message(call.message.chat.id, "🗑 Qaysi sinf jadvalidan darsni o‘chirmoqchisiz?", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("lessondel_"))
    def delete_lesson_day(call):
        if call.message.chat.id not in ADMINS: return
        class_id = call.data.split("_")[1]
        kb = types.InlineKeyboardMarkup()
        days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"]
        for d in days:
            kb.add(types.InlineKeyboardButton(text=d, callback_data=f"lessondelday_{class_id}_{d}"))
        bot.send_message(call.message.chat.id, "📅 Haftaning kunini tanlang:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("lessondelday_"))
    def delete_lesson_finish(call):
        if call.message.chat.id not in ADMINS: return
        _, class_id, day = call.data.split("_")
        db.delete_schedule(class_id, day)
        bot.edit_message_text(f"✅ {day} kuni uchun jadval o‘chirildi.",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)

    # --- EDIT LESSON ---
    @bot.callback_query_handler(func=lambda call: call.data.startswith("lesson_edit"))
    def edit_lesson_start(call):
        if call.message.chat.id not in ADMINS: return
        classes = db.get_classes()
        if not classes:
            bot.send_message(call.message.chat.id, "❌ Hali sinflar yo‘q.")
            return
        kb = types.InlineKeyboardMarkup()
        for c in classes:
            kb.add(types.InlineKeyboardButton(text=c[1], callback_data=f"lessonedit_{c[0]}"))
        bot.send_message(call.message.chat.id, "✏️ Qaysi sinf jadvalini o‘zgartirmoqchisiz?", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("lessonedit_"))
    def edit_lesson_day(call):
        if call.message.chat.id not in ADMINS: return
        class_id = call.data.split("_")[1]
        kb = types.InlineKeyboardMarkup()
        days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"]
        for d in days:
            kb.add(types.InlineKeyboardButton(text=d, callback_data=f"lessoneditday_{class_id}_{d}"))
        bot.send_message(call.message.chat.id, "📅 Haftaning kunini tanlang:", reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("lessoneditday_"))
    def edit_lesson_finish(call):
        if call.message.chat.id not in ADMINS: return
        _, class_id, day = call.data.split("_")
        msg = bot.send_message(call.message.chat.id, f"✏️ {day} uchun yangi darslarni kiriting (vergul bilan ajrating):")
        bot.register_next_step_handler(msg, lambda m: save_edit_lesson(m, class_id, day))

    def save_edit_lesson(message, class_id, day):
        lessons = [l.strip() for l in message.text.strip().split(",")]
        db.update_schedule(class_id, day, lessons)
        bot.send_message(message.chat.id, "✅ Jadval yangilandi.")
