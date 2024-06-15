import json
import mysql.connector
from mysql.connector import Error
import pymysql 



class DB:
    def db_conn():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="admin",
                passwd="admin",
                database="WS-AI-VS"
            )
            return connection
        except Error as e:
            print(f"Fehler bei der Datenbankverbindung: {e}")

    def insert_video(path, tags):
        print("path: "+ path + "tags: " + tags)
        connection = DB.db_conn()
        try:
            with connection.cursor() as cursor:
                # Convert tags list to JSON string
                #                     tags_json = json.dumps(tags)
                cursor.execute("INSERT INTO videos (pfad, tags) VALUES (%s, %s)", (path, tags))
                connection.commit()
                print("Zeile erfolgreich hinzugefügt")
        except Error as e:
            print(f"Fehler beim Einfügen der Zeile: {e}")
        finally:
            connection.close()

    def all_videos():
        connection = DB.db_conn()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT pfad FROM videos")
                myresult = cursor.fetchall()
            # Generate HTML video elements for each path
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
        finally:
            if connection.is_connected():
                connection.close()
# Example usage
# DB.insert_video("/path/to/video.mp4", ["tag1", "tag2", "tag3"])