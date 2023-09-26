from models.model import *


def user_create(msg):
    try:
        telegram_id = msg.from_user.id
        username = msg.from_user.username
        first_name = msg.from_user.first_name
        if user := get_user(telegram_id):
            return user
        else:
            return create_user(telegram_id=telegram_id, username=username, first_name=first_name)
    except:
        return None


def all_users(msg):
    try:
        data = statistika()
        return f"Assalomu alaykum {msg.from_user.first_name}\nBugun qo'shildi: {data['day'].count()}\nBir hafta ichida qo'shildi: {data['week'].count()}\nBir oyda qo'shildi: {data['month'].count()}\n\nBu siz uchun statistika!"
    except:
        return None

