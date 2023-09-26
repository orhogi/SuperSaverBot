from models.model import User, InstaLikeeTik, Pin

user = User('users')
insta = InstaLikeeTik('instagram')
tiktok = InstaLikeeTik('tiktok')
likee = InstaLikeeTik('likee')
pin = Pin('pinterest')


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


def all_users():
    try:
        data = user.get_medias()
        return data
    except:
        return None


def user_statistic():
    data = user.statistika()
    return f"Bu oyda jami qo'shilganlar Soni: {len(data['month'])}\nBu hafta jami qo'shilganlar Soni: {len(data['week'])}\nBugun jami qo'shilganlar Soni: {len(data['day'])}"


def media_statistic():
    insta_stat = insta.statistika()
    tiktok_stat = tiktok.statistika()
    likee_stat = likee.statistika()
    pin_stat = pin.statistika()
