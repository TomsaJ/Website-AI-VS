import json
import mysql.connector
from mysql.connector import Error

class DB:
    @staticmethod
    def load_db_config():
        with open('db_config.json', 'r') as file:
            config = json.load(file)
        return config

    @classmethod
    def db_connection(cls):
        connection = None
        db_config = cls.load_db_config()
        try:
            connection = mysql.connector.connect(
                host=db_config['host'],
                user=db_config['user'],
                passwd=db_config['password'],
                database=db_config['database']
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

    @classmethod
    def insert_video(cls, path, tags):
        connection = cls.db_connection()
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
