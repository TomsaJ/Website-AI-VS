import os
import re  # Für die Eingabevalidierung
import shutil
import mysql.connector
from mysql.connector import Error
from .file import FileManager


class Db:
    @staticmethod
    def sanitize_input(input_str):
        if isinstance(input_str, str):
            # Removes all unwanted characters from the input
            sanitized_str = re.sub(r'[^\w\s\-\\\/\.]', '', input_str)
            return sanitized_str
        else:
            # If it is not a string, return the input unchanged
            return input_str


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

    def insert_video(path, user, folder, time):
        connection = Db.db_conn()
        if connection is None:
            return "Connection to the database failed."
        try:
            with connection.cursor() as cursor:
                sanitized_path = Db.sanitize_input(path)
                sanitized_user = Db.sanitize_input(user)
                sanitized_folder = Db.sanitize_input(folder)

                cursor.execute(
                    "INSERT INTO videos (path, user, folder, time) VALUES (%s, %s, %s, %s)",
                    (sanitized_path, sanitized_user, sanitized_folder, time)
                )
                connection.commit()
                print("Zeile erfolgreich hinzugefügt")
        except Error as e:
            print(f"Fehler beim Einfügen der Zeile: {e}")
        finally:
            connection.close()

    def get_videos(user):
        connection = Db.db_conn()
        if user == "null":
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT path FROM videos")
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
                sanitized_user = Db.sanitize_input(user)
                with connection.cursor() as cursor:
                    sql_query = "SELECT path, folder FROM videos WHERE user = %s"
                    cursor.execute(sql_query, (sanitized_user,))
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

    def get_all_lang():
        connection = Db.db_conn()
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
        connection = Db.db_conn() 
        if connection is None:
            return None  # Return None to indicate that the connection could not be established
        try:
            sanitized_lang = Db.sanitize_input(lang)
            with connection.cursor() as cursor:
                sql_query = "SELECT language_code FROM language WHERE language_name = %s"
                cursor.execute(sql_query, (sanitized_lang,))
                myresult = cursor.fetchone()  # Since we expect only one value, use fetchone()
                if myresult:
                    return myresult[0]  # Return the first element of the tuple (language_code)
                else:
                    return None  # Return None if no result is found
        except Error as e:
            print(f"Error fetching data: {e}")
            return None  # Return None in case of an error
        finally:
            if connection.is_connected():
                connection.close()  # Close the database connection if it is open

    def register_user(username, password):
        connection = Db.db_conn()
        try:
            sanitized_username = Db.sanitize_input(username)
            sanitized_password = Db.sanitize_input(password)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO user (username, password) VALUES (%s, %s)",
                    (sanitized_username, sanitized_password)
                )
                connection.commit()
                return True
        except Error as e:
            return False
        finally:
            connection.close()

    def login_user(username, password):
        connection = Db.db_conn()
        if connection is None:
            return None  # Return None to indicate that the connection could not be established
        try:
            sanitized_username = Db.sanitize_input(username)

            cursor = connection.cursor()
            sql_query = "SELECT password FROM user WHERE username = %s"
            cursor.execute(sql_query, (sanitized_username,))
            myresult = cursor.fetchone()
            return myresult
        except Error as e:
            print(f"Error fetching data: {e}")
            return None  # Return None in case of an error
        finally:
            cursor.close()
            if connection.is_connected():
                connection.close()  # Close the database connection if it is open

    def delete_video(time):
        connection = Db.db_conn()
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
                        print("gelöscht")
        except Error as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return "<p>Empty</p>"
        finally:
            if connection.is_connected():
                connection.close()
