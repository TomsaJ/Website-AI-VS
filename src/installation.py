import sys
import os
src_path = "/src"
sys.path.append(src_path)
from file import FileManager as file
from timer import Time as time
from design import ProgramDesign

class Installation:
    @staticmethod
    def startup():
        file.delete_tmp_folder()
        file.delete_tmp_file("src/time.csv")
        print("Die Installation wird gestartet bitte warten ...")
        # Assuming jsonfile() is defined outside of TempFileManager class
        paths = ['1min.mp4','10min.mp4','15min.mp4', '20min.mp4', '30min.mp4']
        time.fillfile(paths)
        installtatio_neede_time = time.calculate_average()
        file.jsonfile(installtatio_neede_time)
        print("Installation beendet")
        ProgramDesign.lines()
        file.delete_tmp_folder()
        file.delete_tmp_file("src/time.csv")
if __name__ == "__main__":
    Installation.startup()
        #0.1220757381170537