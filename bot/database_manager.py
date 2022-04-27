import sqlite3

def dict_from_row(row):
    return dict(zip(row.keys(), row))

class DBManager(object):
    def __init__(self):
        self.database_name = 'training-bot.db'
        self.__create_tables()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)

        return conn

    def __create_tables(self):
        connection = self.create_connection(self.database_name)
        database = connection.cursor()
        # User (ID, Username)
        database.execute("CREATE TABLE if not exists user (id INTEGER PRIMARY KEY, username TEXT)")
        database.execute("CREATE TABLE if not exists training (user_id INTEGER PRIMARY KEY, training_name TEXT, FOREIGN KEY (user_id) REFERENCES user (id))")
        database.execute("CREATE TABLE if not exists exercise (user_id INTEGER PRIMARY KEY, bench_press INTEGER, deadlift INTEGER, squat INTEGER, clean INTEGER, snatch INTEGER, jerk INTEGER, FOREIGN KEY (user_id) REFERENCES user (id))")
        connection.commit()
        connection.close()

    def get_user(self, user_id):
        connection = self.create_connection(self.database_name)
        connection.row_factory = sqlite3.Row
        database = connection.cursor()
        query = database.execute(f"SELECT id, username FROM user WHERE id = {user_id}").fetchall()
        connection.commit()
        connection.close()
        try:
            if query:
                return dict_from_row(query[0])
        except ValueError:
            return None

    def insert_user(self, user_id, username):
        connection = self.create_connection(self.database_name)
        database = connection.cursor()
        database.execute(f"INSERT INTO user VALUES ({user_id}, '{username}')")
        connection.commit()
        connection.close()
    
    def get_training(self, user_id):
        connection = self.create_connection(self.database_name)
        connection.row_factory = sqlite3.Row
        database = connection.cursor()
        query = database.execute(f"SELECT user_id, training_name FROM training WHERE user_id = {user_id}").fetchall()
        connection.commit()
        connection.close()
        try:
            if query:
                result = dict_from_row(query[0])
                return result['training_name']
        except ValueError:
            return None

    def insert_training(self, user_id, training_name):
        connection = self.create_connection(self.database_name)
        database = connection.cursor()
        database.execute(f"INSERT INTO training VALUES ({user_id}, '{training_name}')")
        connection.commit()
        connection.close()
    
    def update_training(self, user_id, training_name):
        connection = self.create_connection(self.database_name)
        database = connection.cursor()
        database.execute(f"UPDATE training SET training_name = '{training_name}' WHERE user_id = {user_id}")
        connection.commit()
        connection.close()
    
    def insert_exercise(self, user_id):
        connection = self.create_connection(self.database_name)
        database = connection.cursor()
        database.execute(f"INSERT INTO exercise(user_id) VALUES ({user_id})")
        connection.commit()
        connection.close()

    def get_exercise(self, user_id, exercise_name):
        connection = self.create_connection(self.database_name)
        connection.row_factory = sqlite3.Row
        database = connection.cursor()
        query = database.execute(f"SELECT {exercise_name} FROM exercise WHERE user_id = {user_id}").fetchall()
        connection.commit()
        connection.close()
        try:
            if query:
                result = dict_from_row(query[0])
                return result[f'{exercise_name}']
        except ValueError:
            return None
    
    def update_exercise(self, user_id, column_name, exercise_rm):
        connection = self.create_connection(self.database_name)
        database = connection.cursor()
        database.execute(f"UPDATE exercise SET {column_name} = {exercise_rm} WHERE user_id = {user_id}")
        connection.commit()
        connection.close()