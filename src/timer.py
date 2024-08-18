import asyncio
import os
import sys
import time
from moviepy.editor import VideoFileClip
from .subtitle_gen import SubtitleGen
from .file import FileManager


class Time:

    @staticmethod
    def add_newfac(new_d , duration):
        new_time = new_d/duration
        old_f = FileManager.readjson()
        new_f = (old_f + new_time)/2
        FileManager.writejsonfile(new_f)

    @staticmethod
    async def timer():
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            print("Elapsed Time: {:.2f} seconds".format(elapsed_time))
            await asyncio.sleep(1)  # Wait 1 second

    @staticmethod
    async def async_method():
        filename = 'time.csv'
        await Time.calculate_average(filename)

    @staticmethod
    def calculate_average():
        filename = os.path.join(os.getcwd(), 'src', 'time.csv')
        total = 0
        count = 0
        with open(filename, 'r') as file:
            for line in file:
                # Split the line based on semicolon
                values = line.strip().split(';')
                # Extract the first and second value as floats
                first_value, second_value = map(float, values)
                # Add the result to the total sum
                total += first_value / second_value
                count += 1
        # Calculate the average
        average = total / count 
        return average

    @staticmethod
    def fill_file(paths):
        ini_time = time.time()
        i = 0
        for file_path in paths:
            # Process the video
            execution_time, video_duration = Time.process_video(file_path)
            
            # Write results to CSV
            Time.write_to_csv(execution_time, video_duration, i)
            
            # Estimate installation time
            if i == 0:
                time_init = Time.estimate_installation_time(execution_time, video_duration)
                i = 1

            # Calculate and display progress
            sum_time = (time.time() - ini_time) / 60
            if (sum_time / time_init) * 100 <= 100:
                print(f'Es sind schon {((sum_time) / time_init) * 100: .2f} % installiert ...')
        
        print('100 % ')

    @staticmethod
    def process_video(file_path):
        file = os.path.join(os.getcwd(), 'video', file_path)
        filename = 'tmp'
        file = FileManager.copy_to_tmp_directory(file, filename)
        start_time = time.time()
        # Generate subtitles for the video
        asyncio.run(SubtitleGen.untertitel(file, filename))
        output_file = os.path.join(os.getcwd(), filename, file_path + '_subtitle.mp4')
        subtitle = os.path.join(os.getcwd(), filename, filename + '_subtitle.srt')
        FileManager.combine_video_with_subtitle(file, subtitle, output_file)
        end_time = time.time()
        execution_time = end_time - start_time
        clip = VideoFileClip(file)
        video_duration = clip.duration
        clip.close()
        return execution_time, video_duration

    @staticmethod
    def write_to_csv(execution_time, video_duration, index):
        csv_file_path = os.path.join(os.getcwd(), "src", 'time.csv')
        mode = 'w' if index == 0 else 'a'
        with open(csv_file_path, mode) as file:
            file.write(f'{execution_time};{video_duration}\n')

    @staticmethod
    def estimate_installation_time(execution_time, video_duration):
        time_init = ((execution_time / video_duration) * (60 * 60)) / 60
        print(f'Die Installation wird {time_init % 60: .2f} Minuten dauern')
        print("...")
        return time_init

    @staticmethod
    def duration(video_duration, d):
        print(f"Dauert: {(video_duration * d)/60:.2f} Minuten")
        d = ((video_duration * d)/60)
        return d


