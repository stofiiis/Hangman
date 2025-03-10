import sqlite3

class Db_base:
    def __init__(self):
        self.path = "database.db"
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def refresh(self):
        self.path = "database.db"
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def c_execute(self, sql, params=()):
        self.refresh()
        self.cursor.execute(sql, params)
        self.connection.commit()

    def fetchall(self):
        result = self.cursor.fetchall()
        self.cursor.close()
        return result


class db_i(Db_base):
    def __init__(self):
        super().__init__()

    def insert_user(self, user, password, score):
        sql = "INSERT INTO users_score (name, password, score) VALUES (?, ?, ?)"
        values = (user, password, score)
        self.c_execute(sql, values)

    def update_score(self, user, new_score):
        sql = "UPDATE users_score SET score = ? WHERE name = ?"
        values = (new_score, user)
        self.c_execute(sql, values)


class db_s(Db_base):
    def __init__(self):
        super().__init__()

    def get_user(self, name):
        sql = "SELECT * FROM users_score WHERE name=?"
        values = (name,)
        self.c_execute(sql, values)
        result = self.fetchall()
        return result

    def get_top_users(self):
        sql = "SELECT name, score FROM users_score ORDER BY score DESC LIMIT 10"
        self.c_execute(sql)
        result = self.fetchall()
        return result


class db(db_i, db_s):
    def __init__(self):
        super().__init__()



