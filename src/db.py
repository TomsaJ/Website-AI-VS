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

    def insert_video(path, user):
        connection = DB.db_conn()
        try:
            with connection.cursor() as cursor:
                # Convert tags list to JSON string
                #                     tags_json = json.dumps(tags)
                cursor.execute("INSERT INTO videos (pfad, user) VALUES (%s, %s)", (path, user))
                connection.commit()
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
                    sql_query = "SELECT pfad FROM videos where user = %s"
                    cursor.execute(sql_query, (user,))
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

    def login(username, password):
        connection = DB.db_conn()
        if connection is None:
            return None  # Rückgabe None, um anzuzeigen, dass keine Verbindung hergestellt werden konnte
        try:
            with connection.cursor() as cursor:
                sql_query = "SELECT password FROM user WHERE username = %s"
                cursor.execute(sql_query, (username,))
                myresult = cursor.fetchone()  # Da wir nur einen Wert erwarten, verwenden wir fetchone()
                if myresult:
                    if password == myresult[0]:
                        return True
                    else:
                        return False   # Rückgabe des ersten Elements des Tupels (language_code)
            cursor = connection.cursor()
            sql_query = "SELECT password FROM user WHERE username = %s"
            cursor.execute(sql_query, (username,))
            myresult = cursor.fetchone()
            if myresult:
                stored_password = myresult[0]
                if password == stored_password:
                    return True
                else:
                    return False
            else:
                return None  # Rückgabe None, wenn kein Ergebnis gefunden wurde
        except Error as e:
            print(f"Error fetching data: {e}")
            return None  # Rückgabe None im Falle eines Fehlers
        finally:
            cursor.close()
            if connection.is_connected():
                connection.close()  # Schließen Sie die Verbindung zur Datenbank, wenn sie geöffnet ist

# Example usage
# DB.insert_video("/path/to/video.mp4", ["tag1", "tag2", "tag3"])