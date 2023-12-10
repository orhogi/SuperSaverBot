from data.crud import channel
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_btn():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistic = KeyboardButton("Statistics 📊")
    reklama = KeyboardButton("Reklama 🗣")
    media_statistic = KeyboardButton("Channels 🖇")
    return btn.add(statistic, reklama, media_statistic)


def channels_btn():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    add_channel = KeyboardButton("Kanal qo'shish ⚙️")
    delete_channel = KeyboardButton("Kanal o'chirish 🗑")
    exits = KeyboardButton("❌")
    return btn.add(add_channel, delete_channel, exits)


def exit_btn():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    exit = KeyboardButton("❌")
    return btn.add(exit)


def forced_channel():
    channels = channel.get_datas()
    btn = InlineKeyboardMarkup(row_width=2)
    for i, v in enumerate(channels):
        btn.add(InlineKeyboardButton(f"{int(i) + 1} - kanal", url=f"https://t.me/{v['username'][1:]}"))
    return btn.add(InlineKeyboardButton("Tekshirish ✅", callback_data="channel_check"))