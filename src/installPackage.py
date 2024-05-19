import subprocess
import sys
from design import ProgramDesign
class PackageInstaller:
    def check_and_install_package(package_name):
        try:
            # Überprüfe, ob das Paket installiert ist
            subprocess.check_output([sys.executable, '-m', 'pip', 'show', package_name])
            #print(f"{package_name} ist bereits installiert.")
        except subprocess.CalledProcessError:
            # Das Paket ist nicht installiert, installiere es
            print(f"{package_name} wird installiert...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', package_name])
            print(f"{package_name} wurde erfolgreich installiert.")

