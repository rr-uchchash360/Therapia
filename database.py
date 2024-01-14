from dbm import _Database
import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'ABRARMAHABUBNOWRID24022002'
        self.database = 'therapia'
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query, data=None):
        try:
            cursor = self.connection.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Error: {e}")
            return None

    def fetch_all(self, query):
        cursor = self.execute_query(query)
        if cursor:
            return cursor.fetchall()
        else:
            return []

    def fetch_one(self, query):
        cursor = self.execute_query(query)
        if cursor:
            return cursor.fetchone()
        else:
            return None


db = Database()
db.connect()
