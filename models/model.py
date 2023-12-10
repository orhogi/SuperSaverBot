from db.connection import cur, conn

class User:
    def __init__(self, table) -> None:
        self.table = table

    def create_user(self, telegram_id: int, username: str, first_name: str):
        query = f"INSERT INTO {self.table}(telegram_id, username, first_name) VALUES (%s, %s, %s)"
        cur.execute(query, (str(telegram_id), username, first_name))
        conn.commit()

    def get_user(self, telegram_id: int):
        query = f"SELECT * FROM {self.table} WHERE telegram_id = %s"
        cur.execute(query, (str(telegram_id),))
        return cur.fetchone()

    def get_users(self):
        query = f"SELECT * FROM {self.table}"
        cur.execute(query)
        return cur.fetchall()

    def statistika(self):
        query = f"SELECT * FROM {self.table} WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'"
        cur.execute(query)
        month = cur.fetchall()
        query_week = f"SELECT * FROM {self.table} WHERE created_at >= DATE_TRUNC('week', CURRENT_DATE) - INTERVAL '1 week'"
        cur.execute(query_week)
        week = cur.fetchall()
        query_day = f"SELECT * FROM {self.table} WHERE created_at >= DATE_TRUNC('day', CURRENT_DATE) - INTERVAL '1 day'"
        cur.execute(query_day)
        day = cur.fetchall()
        return {'month': month, 'week': week, 'day': day}
    

class Channel:
    def __init__(self, table) -> None:
        self.table = table

    def create_data(self, username: str):
        query = f"INSERT INTO {self.table}(username) VALUES (%s)"
        cur.execute(query, (username, ))
        conn.commit()
    
    def delete_data(self, username: int):
        query = f"DELETE FROM {self.table} WHERE username = %s"
        cur.execute(query, (username,))
        conn.commit()
    
    def get_data(self, username: int):
        query = f"SELECT * FROM {self.table} WHERE username = %s"
        cur.execute(query, (username,))
        return cur.fetchone()
    
    def get_datas(self):
        query = f"SELECT * FROM {self.table}"
        cur.execute(query)
        return cur.fetchall()
    