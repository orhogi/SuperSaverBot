from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    statistic = KeyboardButton("📊 Statistics")
    reklama = KeyboardButton("🗣 Reklama")
    media_statistic = KeyboardButton("📈 Media Statistics")
    find_user = KeyboardButton("👤 Find User")
    return btn.add(statistic, reklama, find_user, media_statistic)


def exit_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    exit = KeyboardButton("❌")
    return btn.add(exit)
