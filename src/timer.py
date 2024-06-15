import asyncio
import time
import os
import sys
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)
from subtitle_gen import Subtitle_gen
from file import FileManager
from moviepy.editor import VideoFileClip
class Time:
    @staticmethod
    async def timer():
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            print("Elapsed Time: {:.2f} seconds".format(elapsed_time))
            await asyncio.sleep(1)  # Warte 1 Sekunde
    async def async_method():
    # Hier kommt der Code deiner asynchronen Methode
        filename = 'time.csv'
        await Time.calculate_average(filename)
    def calculate_average():
        filename = os.path.join(os.getcwd(), 'src', 'time.csv')
        total = 0
        count = 0
        with open(filename, 'r') as file:
            for line in file:
                # Trenne die Zeile anhand des Semikolons
                values = line.strip().split(';')
                # Extrahiere den ersten und zweiten Wert als Gleitkommazahlen
                first_value, second_value = map(float, values)
                # Füge das Ergebnis zur Gesamtsumme hinzu
                total += first_value / second_value
                count += 1
        # Berechne den Durchschnitt
        average = total / count 
        return average
    def fillfile(paths):
        summe_time = 0
        ini_time = time.time()
        i = 0
        for file_path in paths:
            file = os.path.join(os.getcwd(), 'video', file_path)
            filename = 'tmp'
            file = FileManager.copy_to_tmp_directory(file,filename)
            start_time = time.time()
        # Annahme: Die Funktion untertitel(file_path) erstellt Untertitel für das Video
            asyncio.run(Subtitle_gen.untertitel(file,filename))
            output_file = os.path.join(os.getcwd(), filename,  file_path + '_subtitle.mp4')
            subtitle = os.path.join(os.getcwd(), filename, filename +'_subtitel.srt')
            FileManager.combine_video_with_subtitle(file, subtitle, output_file)
            end_time = time.time()
            execution_time = end_time - start_time
            video_file = file_path
            clip = VideoFileClip(file)
            video_duration = clip.duration
            clip.close()
            csv_file_path = os.path.join(os.getcwd(), "src", 'time.csv')
            if i == 0:
                with open(csv_file_path, 'w') as file:
                    file.write(f'{execution_time};{video_duration}\n')
            else:
                with open(csv_file_path, 'a') as file:
                    file.write(f'{execution_time};{video_duration}\n')
            while i == 0:
                print(f'Die Installation wird {(((execution_time/video_duration)*(60*60))/60)%60: .2f} Minuten dauern' )
                print("...")
                time_init = ((execution_time/video_duration)*(60*60))/60
                i =1
            init_time_end = time.time()
            init_time_end = init_time_end - ini_time
            summe_time = summe_time + (init_time_end/60)
            if ((summe_time)/time_init) * 100 <= 100:
                print (f'Es sind schon {((summe_time)/time_init) * 100: .2f} % installiert ...')
        print('Es sind schon 100 % ')
