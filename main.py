import os
import sys
import shutil
import time
import ssl
import asyncio

src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

async def subtitel(file_path, filename):
        sub = Subtitle_gen()
        # Hier wird untertitel(file_path) aufgerufen oder implementiert
        await sub.untertitel(file_path,filename)
        #await asyncio.sleep(10)
        

def input_path():
    a = False
    while not a: 
        # Fordere den Benutzer auf, den Dateipfad einzugeben
        old_path = input("Geben Sie den Pfad zur Datei ein: ").strip()
        # Überprüfe, ob der angegebene Pfad gültig ist
        if os.path.isfile(old_path):
            filename = FileManager.get_file_name(old_path)
            file_path = FileManager.copy_to_tmp_directory(old_path, filename)
            a = True
        else:
            if old_path == 'e':
                return old_path, 'e', 'e'
            print("Ungültiger Dateipfad.")
    print("Der Untertitel wird nun erzeugt.")
    return file_path, old_path, filename


async def main():
    file_path = ''
    while file_path != 'e':
        print("Programm wird mit e beendet")
        #tmp.delete_tmp_folder() #für das debugging
        file_path, old_path, filename = input_path()
        if file_path == 'e':
            print("Programm wurde beendet")
            return
        video_duration = FileManager.duration_video(file_path)
        d = FileManager.readjson()
        ProgramDesign.duration(video_duration, d)
        #tmp.delete_tmp_file(file_path)
        start_time = time.time()
        task = asyncio.create_task(subtitel(file_path, filename))
        '''timer_task = asyncio.create_task(Tim.timer())'''
        execution_time = await task
        #print("Execution Time:", execution_time)
        '''timer_task.cancel()
        try:
            await timer_task
        except asyncio.CancelledError:
            pass'''
        output_file = FileManager.get_file_name(file_path)
        output_file = os.path.join(os.getcwd(), filename,  output_file + '_subtitle.mp4')
        subtitle = os.path.join(os.getcwd(), filename, filename +'_subtitel.srt')
        FileManager.combine_video_with_subtitle(file_path, subtitle, output_file)
        end_time = time.time()
        execution_time = end_time - start_time
        ProgramDesign.neededtime(execution_time)
        FileManager.delete_tmp_file(file_path)
        t = FileManager.move_tmp_directory_back(old_path,filename)
        ProgramDesign.lines()
        print(f"Das Video hat jetzt einen untertitel und liegt im Verzeichnis\n{old_path.strip('.mp4')}")
        ProgramDesign.lines()
    print("Programm wurde beendet")

if __name__ == "__main__":
    #ssl._create_default_https_context = ssl._create_unverified_context # bei schwierigkeiten mit der SSL verbindung einkommentieren
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from installPackage import PackageInstaller
    print("Programm startet ...")
    PackageInstaller.check_and_install_package('openai-whisper')
    PackageInstaller.check_and_install_package('ffmpeg-python')
    PackageInstaller.check_and_install_package('moviepy')
    from moviepy.editor import VideoFileClip
    from subtitle_gen import Subtitle_gen
    from file import FileManager
    from timer import Time
    from installation import Installation
    from design import ProgramDesign
    json_file_path = "src/data.json"
    info = ProgramDesign()
    # Überprüfen, ob die Datei bereits vorhanden ist
    if not os.path.exists(json_file_path):
        Installation.startup()
    asyncio.run(main())