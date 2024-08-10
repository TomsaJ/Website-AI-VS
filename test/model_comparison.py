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
    for model in a:
        tmp_time = time.time()
        file_location = '10min.mp4'
        file_path = Path(file_location)
        file_name = file_path.name
        filename = FileManager.get_file_name(file_path)
        tmp_file_path = FileManager.copy_to_tmp_directory(file_path, filename)
        FileManager.delete_tmp_file(file_path)
        print(tmp_file_path)
        SubtitleGen.create_subtitles(tmp_file_path, filename, 'German', model)
        output_file = 'test/videos' + model+ PATH_SEPARATOR + filename + '_'+ time.time() + '_subtitle.mp4'
        subtitle = 'test/videos' + model + PATH_SEPARATOR + filename + '_'+ time.time() +  '_subtitle.srt'
        file_path = 'test/videos' + model + PATH_SEPARATOR + filename + '_'+ time.time() +  '.mp4'
        lang = Db.get_language_code(lang)
        FileManager.combine_video_with_subtitle(file_path, subtitle, output_file, 'ger')
        current_time = time.time()
        print("Untertitelerstellungsdauer:")
        print ((current_time - tmp)/1000 + " Sekunden")
        print ((current_time - tmp)/6000 + " Minuten")
    print("Fertig")


if __name__ == "__main__":
    main()