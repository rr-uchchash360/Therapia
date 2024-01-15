import mysql.connector


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234therapia1234',
                database='therapia'
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database")

    def execute_query(self, query, data=None):
        try:
            if not self.connection.is_connected():
                self.connect()  # Reconnect if the connection is lost

            if not self.cursor:
                self.cursor = self.connection.cursor()

            self.cursor.execute(query, data)
            self.connection.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def fetch_data(self, query, data=None):
        try:
            self.cursor.execute(query, data)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
