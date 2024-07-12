import json
from file import FileManager
import os
import shutil


class JS:
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

    def insert_video(path, user, folder, time):
        video_data = {
        "pfad": path,
        "user": user,
        "folder": folder,
        "time": time
    }

        if os.path.exists('video.json'):
        # Lade vorhandene Videos
            with open('video.json', 'r') as file:
                videos = json.load(file)
        else:
        # Wenn die Datei nicht existiert, erstelle eine neue Liste
            videos = []

    # Füge das neue Video zur Liste hinzu
        videos.append(video_data)

    # Speichere die aktualisierte Liste in der video.json Datei
        with open('video.json', 'w') as file:
            json.dump(videos, file, indent=4)

    def videos(user):
        if os.path.exists('video.json'):
        # Lade vorhandene Videos
            with open('video.json', 'r') as file:
                all_videos = json.load(file)
        else:
        # Wenn die Datei nicht existiert, gib eine Nachricht zurück
            return "<p>Keine Videos gefunden</p>"

    # Wenn der Benutzer "null" ist, zeige alle Videos an
        if user == "null":
            video_elements = ''.join([
                f'<video width="320" height="270" controls>'
            f'<source src="{video["pfad"]}" type="video/mp4">'
            'Your browser does not support the video tag.'
            '</video>'
            for video in all_videos
        ])
            return video_elements
        else:
        # Filtere die Videos nach Benutzer
            user_videos = [video for video in all_videos if video["user"] == user]

            if not user_videos:
                return "Noch keine Videos"

            video_elements = ''.join([
                f'<video width="320" height="270" controls>'
            f'<source src="{video["pfad"]}" type="video/mp4">'
            'Your browser does not support the video tag.'
            '</video> <br>'
            f"""
                <button onclick="window.location.href='{video["pfad"]}'" download>Originaldatei herunterladen</button>
                <button onclick="window.location.href='{video["folder"]}/{os.path.splitext(os.path.basename(video["pfad"]))[0]}.srt'" download>Untertitel herunterladen (.srt)</button>
                <button onclick="window.location.href='{video["folder"]}/{os.path.splitext(os.path.basename(video["pfad"]))[0]}_all.txt'" download>Textdatei herunterladen (.txt)</button>
            """
            for video in user_videos
        ])
            return video_elements
    
    def all_lang():
        if os.path.exists('language.json'):
        # Lade vorhandene Sprachen
            with open('language.json', 'r') as file:
                languages = json.load(file)
        else:
        # Wenn die Datei nicht existiert, gib eine leere Zeichenkette zurück
            return ""

    # Erstelle die HTML-Option-Elemente für die Sprachen
        language_elements = ''.join([
            f'<option value="{language.capitalize()}">{language.capitalize()}</option>'
        for language in languages
    ])

        return language_elements
    
    def get_language_code(lang):
        if os.path.exists('language.json'):
        # Lade vorhandene Sprachen und ihre Codes
            with open('language.json', 'r') as file:
                data = json.load(file)
                languages = data.get('languages', [])
        else:
        # Wenn die Datei nicht existiert, gib None zurück
            return None

    # Suche den Sprachcode für die gegebene Sprache
        for language in languages:
            if language['name'] == lang:
                return language['code']

    # Rückgabe None, wenn die Sprache nicht gefunden wurde
        return None

    def login(username, password):
        if os.path.exists('users.json'):
        # Lade vorhandene Benutzerdaten
            with open('users.json', 'r') as file:
                data = json.load(file)
                users = data.get('users', [])
        else:
        # Wenn die Datei nicht existiert, gib None zurück
            return None

    # Suche den Benutzer und überprüfe das Passwort
        for user in users:
            if user['username'] == username:
                if user['password'] == password:
                    return True
                else:
                    return False

    # Rückgabe None, wenn der Benutzer nicht gefunden wurde
        return None
    
    def delete_Video(time):
        thirty_days_in_seconds = 30 * 24 * 60 * 60
        thirty_days_in_milliseconds = thirty_days_in_seconds * 1000

        if os.path.exists('video.json'):
        # Lade vorhandene Videos
            with open('video.json', 'r') as file:
                videos = json.load(file)
        else:
        # Wenn die Datei nicht existiert, gib eine Nachricht zurück
            return "<p>Keine Videos gefunden</p>"

        videos_to_delete = []
        for video in videos:
            video_time = datetime.strptime(video["time"], '%Y-%m-%dT%H:%M:%SZ')
            video_timestamp = int(video_time.timestamp()) * 1000

            if time - video_timestamp >= thirty_days_in_milliseconds:
                videos_to_delete.append(video)

        if videos_to_delete:
            for video in videos_to_delete:
            # Lösche das Video aus der JSON-Datei
                videos.remove(video)

            # Lösche den Ordner, falls er existiert
                folder_path = video["folder"]
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path)
                    print(f"Ordner {folder_path} wurde gelöscht.")

        # Speichere die aktualisierte Liste in der video.json Datei
            with open('video.json', 'w') as file:
                json.dump(videos, file, indent=4)

            return f"{len(videos_to_delete)} Videos und Ordner wurden erfolgreich gelöscht."
        else:
            return "Keine Videos gefunden, die gelöscht werden müssen."

# Example usage
# DB.insert_video("/path/to/video.mp4", ["tag1", "tag2", "tag3"])