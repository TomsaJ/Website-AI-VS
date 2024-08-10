import os
import sys
src_path = "../src"
sys.path.append(src_path)
from subtitle_gen import SubtitleGen
from file import FileManager
import time
from pathlib import Path
import ssl

PATH_SEPARATOR = '\\' if os.name == 'nt' else '/'

def main():
    a = ['tiny', 'base', 'small', 'medium', 'large']
    v = ['1min.mp4','10min.mp4','15min.mp4', '20min.mp4', '30min.mp4', '45min.mp4', '90min.mp4']
    print("Current Model;Video; Sekunden; Minuten; ")
    for model in a:
        for video in v:
            
            tmp_time = time.time()
            file_location = video
            file_path = Path(file_location)
            file_name = file_path.name
            filename = FileManager.get_file_name(file_path)
            tmp_file_path = FileManager.copy_to_tmp_directory(file_path, filename)
            SubtitleGen.create_subtitles(tmp_file_path, filename, 'German', model)
            output_file = 'test/videos' + PATH_SEPARATOR + filename + '_subtitle.mp4'
            subtitle = 'test/videos'  + PATH_SEPARATOR + filename  +  '_subtitle.srt'
            file_path = 'test/videos'  + PATH_SEPARATOR + filename  +  '.mp4'
            FileManager.combine_video_with_subtitle(file_path, subtitle, output_file, 'ger')
            current_time = time.time()
            print (model + ";"+ video + ";" + str((current_time - tmp_time)) + ";" + str((current_time - tmp_time)/60)+";")


if __name__ == "__main__":
    main()