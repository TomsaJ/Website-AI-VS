import mysql.connector
from mysql.connector import Error

class DB:

    def load_db_config():
        with open('db_config.json', 'r') as file:
            config = json.load(file)
        return config

    def dbConnection():
        connection = None
        db_config = load_db_config(config_file_path)
        try:
    # Verbindung herstellen
            connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            passwd=config['password'],
            database=config['database']
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



