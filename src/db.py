import os
import json
import mysql.connector
from mysql.connector import Error

class DB:
    @staticmethod
    def db_conn():
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "admin"),
                passwd=os.getenv("DB_PASSWORD", "admin"),
                database=os.getenv("DB_NAME", "WS-AI-VS")
            )
            if connection.is_connected():
                return connection
            else:
                print("Connection failed")
                return None
        except Error as e:
            print(f"Fehler bei der Datenbankverbindung: {e}")
            return None

    @staticmethod
    def insert_video(path, tags):
        print("path: "+ path + "tags: " + tags)
        connection = DB.db_conn()
        if connection is None:
            return "Connection to the database failed."
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO videos (pfad, tags) VALUES (%s, %s)", (path, tags))
                connection.commit()
                print("Zeile erfolgreich hinzugefügt")
        except Error as e:
            print(f"Fehler beim Einfügen der Zeile: {e}")
        finally:
            connection.close()

    @staticmethod
    def all_videos():
        connection = DB.db_conn()
        if connection is None:
            return "Connection to the database failed."
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT pfad FROM videos")
                myresult = cursor.fetchall()
                video_elements = ''.join([
                    f'<video width="320" height="270" controls>'
                    f'<source src="{x[0]}" type="video/mp4">'
                    'Your browser does not support the video tag.'
                    '</video>'
                    for x in myresult
                ])
            return video_elements
        except Error as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return ""
        finally:
            if connection.is_connected():
                connection.close()

# Example usage
# DB.insert_video("/path/to/video.mp4", ["tag1", "tag2", "tag3"])
