import os
import shutil
import subprocess
import zipfile
import ffmpeg
from vtt_to_srt.vtt_to_srt import ConvertFile

from moviepy.editor import VideoFileClip

class FileManager:
    @staticmethod
    def copy_to_tmp_directory(file_path, filename):
        # Create a temporary folder in the current directory
        tmp_folder = 'videos/' + filename
        os.makedirs(tmp_folder, exist_ok=True)
        # Extract the file name from the provided path
        file_name = os.path.basename(file_path)
        # Construct the destination path in the temporary folder
        destination_path = os.path.join(tmp_folder, file_name)
        try:
            # Copy the file to the temporary folder
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
    def move_tmp_directory_back(destination_path, folder_name):
        try:
            destination_path = os.path.dirname(destination_path)
            # Construct the destination path for the temporary folder in the original directory
            original_tmp_folder_path = os.path.join(destination_path, folder_name)
        
            # Move the temporary folder back to the original directory
            shutil.move(folder_name, original_tmp_folder_path)
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten beim Zurückverschieben des temporären Ordners: {e}")
        return destination_path

    @staticmethod
    def delete_tmp_folder(folder_path):
        try:
            shutil.rmtree(folder_path)
            '''print("Der Ordner 'tmp' wurde erfolgreich gelöscht.")
        except FileNotFoundError:
            print("Der Ordner 'tmp' wurde nicht gefunden.")
        except PermissionError:
            print("Keine Berechtigung zum Löschen des Ordners 'tmp'.")'''
        except Exception as e:
            print("Ein Fehler ist beim Löschen des Ordners 'tmp' aufgetreten:", e)
            return

    @staticmethod
    def delete_tmp_file(file_path):  # Path to the file to be deleted
        try:
            os.remove(file_path)
            print("The file 'file.txt' has been successfully deleted.")
        except Exception as e:
            print("An error occurred while deleting the file 'file.txt':", e)
            return

    @staticmethod
    def get_file_name(file_path):
        # Extract the file name from the file path
        file_name_with_extension = os.path.basename(file_path)
        # Separate the file name and the extension
        file_name, file_extension = os.path.splitext(file_name_with_extension)
        # Return the file name
        return file_name

    @staticmethod
    def convert_subtitle_me(subtitle_file):
        convert_file = ConvertFile(subtitle_file, "utf-8")
        convert_file.convert()

    @staticmethod
    def combine_video_with_subtitle(video_file, subtitle_file, output_file, lang):
        # Check if the files exist
        if not os.path.exists(video_file):
            print("Video file not found.")
            return
        if not os.path.exists(subtitle_file):
            print("Subtitle file not found.")
            return
        print(lang)
        cmd = [
            "ffmpeg",
            "-i", video_file,
            "-i", subtitle_file,
            "-c:v", "copy",
            "-c:a", "copy",
            "-c:s", "mov_text",
            "-map", "0:v:0",
            "-map", "0:a:0",
            "-map", "1:s:0",
            "-metadata:s:s:0", "language=" + lang,
            output_file
        ]
        # Execute the FFmpeg command
        with open(os.devnull, 'w') as devnull:
            subprocess.run(cmd, stdout=devnull, stderr=subprocess.STDOUT)

    @staticmethod
    def duration_video(video_file):
        clip = VideoFileClip(video_file)
        video_duration = clip.duration
        clip.close()
        return video_duration

    def create_zip(folder_path):
        # Create a ZIP file from the folder
        zip_file_path = f"{folder_path}.zip"
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
        return zip_file_path
