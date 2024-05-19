import os
import shutil
import ffmpeg
import subprocess
import json
from moviepy.editor import VideoFileClip

class FileManager:
    @staticmethod
    def copy_to_tmp_directory(file_path, filename):
        # Erstelle einen temporären Ordner im aktuellen Verzeichnis
        tmp_folder = os.path.join(os.getcwd(), filename)
        os.makedirs(tmp_folder, exist_ok=True)
        # Extrahiere den Dateinamen aus dem angegebenen Pfad
        file_name = os.path.basename(file_path)
        # Konstruiere den Ziel-Pfad im temporären Ordner
        destination_path = os.path.join(tmp_folder, file_name)
        try:
            # Kopiere die Datei in den temporären Ordner
            shutil.copy(file_path, destination_path)
            '''print(f"Die Datei wurde erfolgreich nach {destination_path} kopiert.")
        except FileNotFoundError:
            print("Die angegebene Datei existiert nicht.")
        except PermissionError:
            print("Zugriff verweigert. Überprüfen Sie die Berechtigungen.")'''
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
        return destination_path
    
    @staticmethod
    def move_tmp_directory_back(ziel_pfad, ordnername):
        try:
            ziel_pfad = os.path.dirname(ziel_pfad)
        # Konstruiere den Ziel-Pfad für den temporären Ordner im ursprünglichen Verzeichnis
            originaler_tmp_ordner_pfad = os.path.join(ziel_pfad, ordnername)
        
        # Verschiebe den temporären Ordner zurück ins ursprüngliche Verzeichnis
            shutil.move(ordnername, originaler_tmp_ordner_pfad)
            #print(f"Der temporäre Ordner wurde erfolgreich zurückverschoben nach {originaler_tmp_ordner_pfad}.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten beim Verschieben des temporären Ordners zurück: {e}")
        return ziel_pfad

    @staticmethod
    def delete_tmp_folder():
        folder_path = "tmp"  # Pfad zum zu löschenden Ordner
        try:
            shutil.rmtree(folder_path)
            '''print("Der Ordner 'tmp' wurde erfolgreich gelöscht.")
        except FileNotFoundError:
            print("Der Ordner 'tmp' wurde nicht gefunden.")
        except PermissionError:
            print("Keine Berechtigung zum Löschen des Ordners 'tmp'.")'''
        except Exception as e:
            # print("Ein Fehler ist beim Löschen des Ordners 'tmp' aufgetreten:", e)
            return

    @staticmethod
    def delete_tmp_file(file_path):  # Path to the file to be deleted
        try:
            os.remove(file_path)
            #print("The file 'file.txt' has been successfully deleted.")
        except Exception as e:
            #print("An error occurred while deleting the file 'file.txt':", e)
            return

    @staticmethod
    def get_file_name(file_path):
        # Extrahiere den Dateinamen aus dem Dateipfad
        file_name_with_extension = os.path.basename(file_path)
        # Trenne den Dateinamen und die Erweiterung
        file_name, file_extension = os.path.splitext(file_name_with_extension)
        # Gib den Dateinamen zurück
        return file_name

    @staticmethod
    def convert_subtitle_me(subtitle_file):
        from vtt_to_srt.vtt_to_srt import ConvertFile

        convert_file = ConvertFile(subtitle_file, "utf-8")
        convert_file.convert()

    @staticmethod
    def combine_video_with_subtitle(video_file, subtitle_file, output_file):
    # Überprüfen, ob die Dateien existieren
        if not os.path.exists(video_file):
            print("Video file not found.")
            return
        if not os.path.exists(subtitle_file):
            print("Subtitle file not found.")
            return
        # ffmpeg-python
        #Funktionert leider nicht wie gewünscht. Gerne selber einwenig experimentieren
        #(ffmpeg
        #.input(video_file)
        #.output(output_file, vcodec='copy', acodec='copy', scodec='mov_text', **{'metadata:s:s:0': 'language=ger'})
        #.output(subtitle_file, **{'metadata:s:s:0': 'language=ger'})
        #.run())
        # FFmpeg-Befehl zum Kombinieren von Video und Untertiteln
        cmd =   [
                "ffmpeg",
                "-i", video_file,
                "-i", subtitle_file,
                "-c:v", "copy",
                "-c:a", "copy",
                "-c:s", "mov_text",
                "-map", "0:v:0",
                "-map", "0:a:0",
                "-map", "1:s:0",
                "-metadata:s:s:0", "language=ger", output_file
                ]
    # FFmpeg-Befehl ausführen
        with open(os.devnull, 'w') as devnull:
            subprocess.run(cmd, stdout=devnull, stderr=subprocess.STDOUT)

    @staticmethod
    def jsonfile(neededtime):
        json_file_path = "src/data.json"
        if os.path.exists(json_file_path):
            return
        else:
            data = {"duration": neededtime}
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file)

    @staticmethod
    def readjson():
        with open("src/data.json", "r") as json_file:
            loaded_data = json.load(json_file)
        selected_value = loaded_data.get("duration")
        return selected_value

    @staticmethod
    def duration_video(video_file):
        clip = VideoFileClip(video_file)
        video_duration = clip.duration
        clip.close()
        return video_duration