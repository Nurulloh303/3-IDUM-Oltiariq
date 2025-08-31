import sqlite3

class DB:
    DB_NAME = "database.db"

    # === BAZA ULANISH ===
    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB.DB_NAME)
        cursor = conn.cursor()
        return conn, cursor

    # === FOYDALANUVCHI ===
    @staticmethod
    def get_user(user_id):
        conn, cursor = DB.get_connection()
        cursor.execute("SELECT * FROM users WHERE chat_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def add_user(chat_id, full_name, phone):
        conn, cursor = DB.get_connection()
        cursor.execute("INSERT INTO users (chat_id, full_name, phone) VALUES (?, ?, ?)",
                       (chat_id, full_name, phone))
        conn.commit()
        conn.close()

    @staticmethod
    def update_user_name(chat_id, full_name):
        conn, cursor = DB.get_connection()
        cursor.execute("UPDATE users SET full_name = ? WHERE chat_id = ?", (full_name, chat_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update_user_class(chat_id, class_id):
        conn, cursor = DB.get_connection()
        cursor.execute("UPDATE users SET class_id = ? WHERE chat_id = ?", (class_id, chat_id))
        conn.commit()
        conn.close()

    # === SINFLAR ===
    @staticmethod
    def get_classes():
        conn, cursor = DB.get_connection()
        cursor.execute("SELECT * FROM classes")
        classes = cursor.fetchall()
        conn.close()
        return classes

    @staticmethod
    def add_class(name):
        conn, cursor = DB.get_connection()
        cursor.execute("INSERT INTO classes (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_class(class_id):
        conn, cursor = DB.get_connection()
        cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_class(class_id, name):
        conn, cursor = DB.get_connection()
        cursor.execute("UPDATE classes SET name = ? WHERE id = ?", (name, class_id))
        conn.commit()
        conn.close()

    # === DARS JADVALI ===
    @staticmethod
    def add_schedule(class_id, day, lessons):
        conn, cursor = DB.get_connection()
        lessons_text = ",".join(lessons)
        cursor.execute("INSERT INTO schedule (class_id, day, lessons) VALUES (?, ?, ?)",
                       (class_id, day, lessons_text))
        conn.commit()
        conn.close()

    @staticmethod
    def get_schedule(class_id, day):
        conn, cursor = DB.get_connection()
        cursor.execute("SELECT lessons FROM schedule WHERE class_id = ? AND day = ?", (class_id, day))
        result = cursor.fetchone()
        conn.close()
        if result:
            return [l.strip() for l in result[0].split(",")]
        return []

    @staticmethod
    def update_schedule(class_id, day, lessons):
        conn, cursor = DB.get_connection()
        lessons_text = ",".join(lessons)
        cursor.execute("UPDATE schedule SET lessons = ? WHERE class_id = ? AND day = ?",
                       (lessons_text, class_id, day))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_schedule(class_id, day):
        conn, cursor = DB.get_connection()
        cursor.execute("DELETE FROM schedule WHERE class_id = ? AND day = ?", (class_id, day))
        conn.commit()
        conn.close()

    # === BAZANI YARATISH ===
    @staticmethod
    def create_tables():
        conn, cursor = DB.get_connection()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            full_name TEXT,
            phone TEXT,
            class_id INTEGER
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER,
            day TEXT,
            lessons TEXT
        )
        """)

        conn.commit()
        conn.close()


# === OB’YEKT YARATISH ===
db = DB()
db.create_tables()
