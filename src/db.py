import json
import mysql.connector
from mysql.connector import Error

class DB:
    def __init__(self):
        self.config = self.load_db_config()

    @staticmethod
    def load_db_config():
        with open('src/db_config.json', 'r') as file:
            config = json.load(file)
        return config

    def db_connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                passwd=self.config['password'],
                database=self.config['database']
            )
            if connection.is_connected():
                print("Erfolgreich verbunden zu MySQL-Datenbank")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                print("Du bist verbunden zu Datenbank:", record)
        except Error as e:
            print("Fehler beim Verbinden zur MySQL-Datenbank", e)
        return connection

    def insert_video(self, path, tags):
        connection = self.db_connection()
        if connection is not None and connection.is_connected():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO videos (pfad, tags) VALUES (%s, %s)", (path, tags))
                    connection.commit()
                    print("Zeile erfolgreich hinzugefügt")
            except Error as e:
                print(f"Fehler beim Einfügen der Zeile: {e}")
            finally:
                connection.close()
        else:
            print("Keine Verbindung zur Datenbank")

# Example usage:
#db_instance = DB()
#db_instance.insert_video('/path/to/video.mp4', 'tag1,tag2,tag3')
