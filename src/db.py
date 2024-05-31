import mysql.connector
from mysql.connector import Error

class DB:
    def dbConnection():    
        try:
    # Verbindung herstellen
            connection = mysql.connector.connect(
            host='dein_host',          # z.B. 'localhost'
            database='deine_datenbank',# Name der Datenbank
            user='dein_benutzername',  # z.B. 'root'
            password='dein_passwort'   # Passwort des Benutzers
        )
            if connection.is_connected():
                print("Erfolgreich verbunden zu MySQL-Datenbank")
                # Einen Cursor erstellen
                cursor = connection.cursor()
                # Eine Abfrage ausführen
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                print("Du bist verbunden zu Datenbank:", record)
        except Error as e:
            print("Fehler beim Verbinden zur MySQL-Datenbank", e)
        return connection

    def insertVideo(path, tags):
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO videos (pfad, tags) VALUES (%s, %s)", (pfad, tags))
            connection.commit()
            print("Zeile erfolgreich hinzugefügt")
        except Error as e:
            print(f"Fehler beim Einfügen der Zeile: {e}")
        finally:
            cursor.close()



