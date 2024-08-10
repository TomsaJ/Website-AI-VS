import subprocess
import sys

class PackageInstaller:
    def check_and_install_package(package_name):
        try:
            # check if a package is already installed
            subprocess.check_output([sys.executable, '-m', 'pip', 'show', package_name])
        except subprocess.CalledProcessError:
            # paket not installed, installation necessary
            print(f"{package_name} wird installiert...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', package_name])
            print(f"{package_name} wurde erfolgreich installiert.")

