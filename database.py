import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("test.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                               user_id integer NOT NULL,
                               firstname nvarchar(30),
                               lastname nvarchar(30),
                               ip_client nvarchar(18),
                               group1 nvarchar,
                               ext_1 nvarchar,
                               ext_2 nvarchar,
                               ext_3 nvarchar,
                               ext_4 nvarchar)
                           """)
        self.conn.commit()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS History(
                               id_incr integer NOT NULL,
                               user_id integer NOT NULL,
                               time datetime NOT NULL,
                               active_app nvarchar NULL,
                               prev_active_app nvarchar NULL,
                               keyboard_input nvarchar NULL,
                               mk_image bool NOT NULL,
                               img_path nvarchar NULL,
                               is_web bool NOT NULL,
                               link nvarchar NULL,
                               order_date date NOT NULL)
                           """)
        self.conn.commit()

    def getting_data_users(self):
        users_data = ['1', '2', '3', '4', '5', 'h', 'e', 'l', 'p']
        self.filling_table_users(users_data)

    def filling_table_users(self, users_data):
        self.cursor.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", users_data)
        self.conn.commit()

    def getting_data_history(self):
        history_data = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', '!']
        self.filling_table_history(history_data)

    def filling_table_history(self, history_data):
        self.cursor.execute("INSERT INTO History VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", history_data)
        self.conn.commit()

    def __del__(self):
        self.conn.close()


database = Database()
database.getting_data_users()
database.getting_data_history()
