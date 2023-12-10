import requests
from models.model import User, Channel
from dotenv import load_dotenv
from os import getenv


user = User('users')
channel = Channel('channels')
load_dotenv(".env")

def user_create(msg):
    try:
        telegram_id = msg.from_user.id
        username = msg.from_user.username
        first_name = msg.from_user.first_name
        if user.get_user(telegram_id):
            return user
        else:
            return user.create_user(telegram_id=telegram_id, username=username, first_name=first_name)
    except:
        return None


def user_statistic():
    data = user.statistika()
    all_user = user.get_users()
    if data:
        return (f"𝐀𝐝𝐦𝐢𝐧 𝐮𝐜𝐡𝐮𝐧 𝐮𝐬𝐞𝐫𝐥𝐚𝐫 𝐒𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐤𝐚𝐬𝐢 🤖📂\n\n"
                f"Oxirgi 30 kun: {len(data['month'])}\n"
                f"Oxirgi 7 kun: {len(data['week'])}\n"
                f"Oxirgi 24 soat: {len(data['day'])}\n\n"
                f"Barcha Userlar soni: {len(all_user)} 📊")
    else:
        return False    


# Channel table data
def create_channel(username: str):
    data = channel.get_data(username)
    if data:
        return False
    else:
        channel.create_data(username)
        return True


def delete_channel(username: str):
    data = channel.get_data(username)
    if data:
        channel.delete_data(username)
        return True
    else:
        return None


def check_channels(telegram_id: int):
    TOKEN = getenv("TOKEN")
    channels = channel.get_datas()
    summa = 0
    try:
        statuses = [requests.get(f'https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={i[1]}&user_id={telegram_id}').json().get('result', {}).get('status', '') for i in channels]
        summa = statuses.count("administrator") + statuses.count("member") + statuses.count("creator")
    except Exception:
        return None

    return summa == len(channels)


def get_channels():
    data = channel.get_datas()
    text = f"Hamkor Kanallar ro'yxati 📥\n\n"
    for i in data:
        text += f"{i['username']}\n"
    return text