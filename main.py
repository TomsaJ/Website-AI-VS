import importlib.util
import logging
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from src.installPackage import PackageInstaller
# Custom module imports
from src.routes import router as main_router  # Import the router from routes.py

# Determine the operating system the application is running on
current_os = os.name

PATH_SEPARATOR = '\\' if current_os == 'nt' else '/'

def install_packages():
    packages = [
        "fastapi",
        "starlette",
        "uvicorn",
        "jinja2",
        "fastapi-sessions"
    ]

    for package in packages:
        PackageInstaller.check_and_install_package(package)


install_packages()

# Configure session secret
config = Config('.env')
SECRET_KEY = config('SECRET_KEY', cast=str, default='your-secret-key')

app = FastAPI() 
logging.basicConfig(level=logging.INFO)
app.add_middleware(SessionMiddleware, secret_key="some-random-secret-key")

# Register the router from routes.py
app.include_router(main_router)

# Directory to store uploaded files
UPLOAD_DIRECTORY = "uploads"
# Ensure the upload directory exists
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Determine the number of available CPUs and use all but one
max_workers = max(1, os.cpu_count() - 1)
executor = ProcessPoolExecutor(max_workers=max_workers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30000)
