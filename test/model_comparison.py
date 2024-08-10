import os
import sys
src_path = "../src"
sys.path.append(src_path)
from subtitle_gen import SubtitleGen
from file import FileManager
import time
from pathlib import Path

import ssl
import urllib.request

try:
    # Veraltete Python-Versionen können diese Methode nicht unterstützen
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Für alte Versionen, die das Attribut nicht haben
    _create_unverified_https_context = None

if _create_unverified_https_context is not None:
    # Setze den unsicheren SSL-Kontext als Standard, wenn verfügbar
    ssl._create_default_https_context = _create_unverified_https_context

# Beispiel für eine HTTP-Anfrage
#response = urllib.request.urlopen('https://example.com')
#print(response.read())


PATH_SEPARATOR = '\\' if os.name == 'nt' else '/'

def main():
    a = ['tiny', 'base', 'small', 'medium', 'large']
    v = ['1min.mp4','10min.mp4','15min.mp4', '20min.mp4', '30min.mp4', '45min.mp4']
    print("Current Model;Video; Sekunden; Minuten; ")
    for model in a:
        for video in v:
            
            tmp_time = time.time()
            file_location = video
            file_path = Path(file_location)
            filename = FileManager.get_file_name(file_path)
            tmp_file_path = FileManager.copy_to_tmp_directory(file_path, filename)
            SubtitleGen.create_subtitles(tmp_file_path, filename, 'German', model)
            current_time = time.time()
            print (model + ";"+ video + ";" + str((current_time - tmp_time)) + ";" + str((current_time - tmp_time)/60)+";")


if __name__ == "__main__":
    main()