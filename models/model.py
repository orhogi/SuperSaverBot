from db.connection import cur, conn


class Base:
    def __init__(self, table):
        self.table = table

    def get_media(self, url: str):
        query = f"SELECT * FROM {self.table} WHERE url = %s"
        cur.execute(query, (url,))
        return cur.fetchone()

    def delete_media(self, url: str):
        query = f"DELETE FROM {self.table} WHERE url = %s"
        cur.execute(query, (url,))
        conn.commit()

    def get_medias(self):
        query = f"SELECT * FROM {self.table}"
        cur.execute(query)
        return cur.fetchall()

    def statistika(self):
        query = f"SELECT * FROM {self.table} WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'"
        cur.execute(query)
        month = cur.fetchall()
        query_day = f"SELECT * FROM {self.table} WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day'"
        cur.execute(query_day)
        day = cur.fetchall()
        query_week = f"SELECT * FROM {self.table} WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '7 day'"
        cur.execute(query_week)
        week = cur.fetchall()
        return {'month': month, 'week': week, 'day': day}


class User(Base):

    def create_user(self, telegram_id: int, username: str, first_name: str):
        query = f"INSERT INTO {self.table}(telegram_id, username, first_name) VALUES (%s, %s, %s)"
        cur.execute(query, (str(telegram_id), username, first_name))
        conn.commit()

    def update_user(self, telegram_id: int, username: str, first_name: str):
        query = f"UPDATE {self.table} SET telegram_id = %s, username = %s, first_name = %s WHERE telegram_id = %s"
        cur.execute(query, (str(telegram_id), username, first_name))
        conn.commit()

    def delete_user(self, telegram_id: int):
        query = f"DELETE FROM {self.table} WHERE telegram_id = %s"
        cur.execute(query, (telegram_id,))
        conn.commit()

    def get_user(self, telegram_id: int):
        query = f"SELECT * FROM {self.table} WHERE telegram_id = %s"
        cur.execute(query, (str(telegram_id),))
        return cur.fetchone()


class Insta(Base):

    def create_media(self, url: str, media: str, post: str, types: str):
        query = f"INSERT INTO {self.table}(url, media, post, types) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (url, media, post, types))
        conn.commit()

    def update_media(self, url: str, media: str, post: str, types: str):
        query = f"UPDATE {self.table} SET url = %s, media = %s, post = %s, types = %s WHERE url = %s"
        cur.execute(query, (url, media, post, url, types))
        conn.commit()


class Pin(Base):
    def create_media(self, url: str, media: str, types: str):
        query = f"INSERT INTO {self.table}(url, media, types) VALUES (%s, %s, %s)"
        cur.execute(query, (url, media, types))
        conn.commit()

    def update_media(self, url: str, media: str, types: str):
        query = f"UPDATE {self.table} SET url = %s, media = %s, post = %s, types = %s WHERE url = %s"
        cur.execute(query, (url, media, types, url))
        conn.commit()


class LikeeTik(Base):
    def create_media(self, url: str, media: str):
        query = f"INSERT INTO {self.table}(url, media) VALUES (%s, %s)"
        cur.execute(query, (url, media))
        conn.commit()

    def update_media(self, url: str, media: str):
        query = f"UPDATE {self.table} SET url = %s, media = %s WHERE url = %s"
        cur.execute(query, (url, media, url))
        conn.commit()


user = User('users')
print(user.get_medias())
