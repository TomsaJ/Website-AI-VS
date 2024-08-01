import os
import json
import mysql.connector
from mysql.connector import Error
import pymysql 
from file import FileManager
import os
import shutil


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
    def insert_video(path, user, folder, time):


        connection = DB.db_conn()
        if connection is None:
            return "Connection to the database failed."
        try:
            with connection.cursor() as cursor:
                # Convert tags list to JSON string
                #                     tags_json = json.dumps(tags)
                cursor.execute("INSERT INTO videos (pfad, user, folder, time) VALUES (%s, %s, %s, %s)", (path, user, folder, time))

                connection.commit()
                print("Zeile erfolgreich hinzugefügt")
        except Error as e:
            print(f"Fehler beim Einfügen der Zeile: {e}")
        finally:
            connection.close()

    def videos(user):
        connection = DB.db_conn()
        if user == "null":
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
                return "<p>Empty</p>"
            finally:
                if connection.is_connected():
                    connection.close()
        else:
            try:
                with connection.cursor() as cursor:
                    sql_query = "SELECT pfad, folder FROM videos WHERE user = %s"
                    cursor.execute(sql_query, (user,))
                    myresult = cursor.fetchall()

                    if not myresult:
                        return "Noch keine Videos"

                    video_elements = ''.join([
                f'<video width="320" height="270" controls>'
                f'<source src="{x[0]}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video> <br>'
                f"""
                    <button onclick="window.location.href='{x[0]}'" download>Originaldatei herunterladen</button>
                    <button onclick="window.location.href='{x[1]}{FileManager.get_file_name(x[0])}.srt'" download>Untertitel herunterladen (.srt)</button>
                    <button onclick="window.location.href='{x[1]}{FileManager.get_file_name(x[0])}_all.txt'" download>Textdatei herunterladen (.txt)</button>
                """


                for x in myresult
                ])
                return video_elements
            except Error as e:
                print(f"Fehler beim Abrufen der Daten: {e}")
                return "<p>Empty</p>"
            finally:
                if connection.is_connected():
                    connection.close()

    def all_lang():
        connection = DB.db_conn()
        if connection is None:
            return ""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT language_name FROM language")
                myresult = cursor.fetchall()
                language_elements = ''.join([
                    f'<option value="{x[0][0].upper() + x[0][1:]}">{x[0][0].upper() + x[0][1:]}</option>'
                    for x in myresult
                ])
            return language_elements
        except Error as e:
            print(f"Error fetching data: {e}")
            return ""
        finally:
            if connection.is_connected():
                connection.close()

    def get_language_code(lang):
        connection = DB.db_conn()  # Annahme: db_conn() stellt die Verbindung zur Datenbank her
        if connection is None:
            return None  # Rückgabe None, um anzuzeigen, dass keine Verbindung hergestellt werden konnte
        try:
            with connection.cursor() as cursor:
                sql_query = "SELECT language_code FROM language WHERE language_name = %s"
                cursor.execute(sql_query, (lang,))
                myresult = cursor.fetchone()  # Da wir nur einen Wert erwarten, verwenden wir fetchone()
                if myresult:
                    return myresult[0]  # Rückgabe des ersten Elements des Tupels (language_code)
                else:
                    return None  # Rückgabe None, wenn kein Ergebnis gefunden wurde
        except Error as e:
            print(f"Error fetching data: {e}")
            return None  # Rückgabe None im Falle eines Fehlers
        finally:
            if connection.is_connected():
                connection.close()  # Schließen Sie die Verbindung zur Datenbank, wenn sie geöffnet ist

    def registration(username, password):
        connection = DB.db_conn()
        try:
            with connection.cursor() as cursor:
                # Convert tags list to JSON string
                #                     tags_json = json.dumps(tags)
                cursor.execute("INSERT INTO user (user, password) VALUES (%s, %s)", (username, password))
                connection.commit()
                return True
        except Error as e:
            return False
        finally:
            connection.close()

    def login(username, password):
        connection = DB.db_conn()
        if connection is None:
            return None  # Rückgabe None, um anzuzeigen, dass keine Verbindung hergestellt werden konnte
        try:
            cursor = connection.cursor()
            sql_query = "SELECT password FROM user WHERE username = %s"
            cursor.execute(sql_query, (username,))
            myresult = cursor.fetchone()
            return myresult
        except Error as e:
            print(f"Error fetching data: {e}")
            return None  # Rückgabe None im Falle eines Fehlers
        finally:
            cursor.close()
            if connection.is_connected():
                connection.close()  # Schließen Sie die Verbindung zur Datenbank, wenn sie geöffnet ist

    def delete_Video(time):
        connection = DB.db_conn()
        thirty_days_in_milliseconds = 30 * 24 * 60 * 60 * 1000
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, folder, time FROM videos")
            myresult = cursor.fetchall()

            for video in myresult:
                video_id = video[0]
                folder_path = video[1]
                video_time = video[2]

                if time - video_time >= thirty_days_in_milliseconds:
                    cursor.execute("DELETE FROM videos WHERE id = %s", (video_id,))
                    connection.commit()
                    if os.path.isdir(folder_path):
                        shutil.rmtree(folder_path)
                        print ("gelöscht")
        except Error as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return "<p>Empty</p>"
        finally:
            if connection.is_connected():
                connection.close()
