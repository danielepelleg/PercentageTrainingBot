import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def dict_from_row(row):
    return dict(zip(row.keys(), row))

class DBManager(object):
    def __init__(self):
        self.DATABASE_NAME = os.environ.get('DATABASE_NAME')
        self.DATABASE_HOST = os.environ.get('DATABASE_HOST')
        self.DATABASE_PORT = os.environ.get('DATABASE_PORT')
        self.DATABASE_USER = os.environ.get('DATABASE_USER')
        self.DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
        self.DATABASE_SSLMODE = os.environ.get('DATABASE_SSLMODE')
        self.__create_tables()

    def create_connection(self):
        """ create a database connection to the SQLite database
        :param db_url: database url
        :return: Connection object or None
        """
        conn = None
        try:
            conn = psycopg2.connect(database = self.DATABASE_NAME,
                                    user = self.DATABASE_USER,
                                    password = self.DATABASE_PASSWORD,
                                    host = self.DATABASE_HOST,
                                    port = self.DATABASE_PORT,
                                    sslmode = self.DATABASE_SSLMODE)
        except psycopg2.Error as e:
            print(e)

        return conn

    def __create_tables(self):
        connection = self.create_connection()
        database = connection.cursor()
        # User (ID, Username)
        database.execute("CREATE TABLE IF NOT EXISTS \"user\" (id INTEGER PRIMARY KEY, username TEXT)")
        database.execute("CREATE TABLE IF NOT EXISTS training (user_id INTEGER PRIMARY KEY, training_name TEXT, FOREIGN KEY (user_id) REFERENCES \"user\" (id))")
        database.execute("CREATE TABLE IF NOT EXISTS exercise (user_id INTEGER PRIMARY KEY, bench_press INTEGER, deadlift INTEGER, back_squat INTEGER, clean INTEGER, snatch INTEGER, jerk INTEGER, front_squat INTEGER, thruster INTEGER, push_press INTEGER, shoulder_press INTEGER, overhead_squat INTEGER, FOREIGN KEY (user_id) REFERENCES \"user\" (id))")
        connection.commit()
        connection.close()

    def get_user(self, user_id):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT id, username FROM \"user\" WHERE id = {user_id}")
        connection.commit()
        result = cursor.fetchone()
        connection.close()
        try:
            if result:
                return {'id': result[0], 'username': result[1]}
        except ValueError:
            return None

    def insert_user(self, user_id, username):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO \"user\" VALUES ({user_id}, '{username}')")
        connection.commit()
        connection.close()
    
    def get_training(self, user_id):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT user_id, training_name FROM training WHERE user_id = {user_id}")
        connection.commit()
        result = cursor.fetchone()
        connection.close()
        try:
            if result:
                return result[1]
        except ValueError:
            return None

    def insert_training(self, user_id, training_name):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO training VALUES ({user_id}, '{training_name}')")
        connection.commit()
        connection.close()
    
    def update_training(self, user_id, training_name):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE training SET training_name = '{training_name}' WHERE user_id = {user_id}")
        connection.commit()
        connection.close()
    
    def insert_exercise(self, user_id):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO exercise(user_id) VALUES ({user_id})")
        connection.commit()
        connection.close()

    def get_exercise(self, user_id, exercise_name):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT {exercise_name} FROM exercise WHERE user_id = {user_id}")
        connection.commit()
        result = cursor.fetchone()
        connection.close()
        try:
            if result:
                print(result[0])
                return result[0]
        except ValueError:
            return None
    
    def update_exercise(self, user_id, column_name, exercise_rm):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE exercise SET {column_name} = {exercise_rm} WHERE user_id = {user_id}")
        connection.commit()
        connection.close()