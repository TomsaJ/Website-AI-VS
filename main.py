import sys
import subprocess
import importlib.util

def install_packages():
    packages = [
        "fastapi",
        "starlette",
        "uvicorn",
        "aiofiles",
        "jinja2"
    ]

    for package in packages:
        if not package_installed(package):
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        else:
            print(f"{package} ist bereits installiert.")

def package_installed(package_name):
    """Überprüft, ob ein Paket installiert ist."""
    package_spec = importlib.util.find_spec(package_name)
    return package_spec is not None

install_packages()
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware
import shutil
import os
import aiofiles
import logging
from fastapi.staticfiles import StaticFiles
from concurrent.futures import ProcessPoolExecutor
from fastapi.templating import Jinja2Templates




app = FastAPI()
logging.basicConfig(level=logging.INFO)
app.add_middleware(SessionMiddleware, secret_key="some-random-secret-key")

# Verzeichnis zum Speichern der hochgeladenen Dateien
UPLOAD_DIRECTORY = "uploads"


# Stelle sicher, dass das Upload-Verzeichnis existiert
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory="page")

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from db import DB
    try:
        videos_html = DB.all_videos()
        return templates.TemplateResponse("index.html", {"request": request, "videos": videos_html})
        #return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)


@app.get("/upload/", response_class=HTMLResponse)
async def upload_page():
    try:
        async with aiofiles.open("page/upload.html", "r") as file:
            content = await file.read()
            return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

# Route, um die Datei zu empfangen und zu verarbeiten
@app.post("/upload_duration/", response_class=HTMLResponse)
async def upload_duration(request: Request, file: UploadFile = File(...), tags: str = Form(...)):
    # Importieren der Module
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from file import FileManager
    from design import ProgramDesign
    print(tags)
    try:
        # Sicherstellen, dass das Upload-Verzeichnis existiert
        upload_dir = UPLOAD_DIRECTORY
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Dateipfad erstellen
        file_location = os.path.join(upload_dir, file.filename)
        
        # Datei speichern
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Video-Dauer berechnen
        video_duration = FileManager.duration_video(file_location)
        duration = ProgramDesign.duration(video_duration, 0.18)
        
        # Erstellen der Antwortseite mit verstecktem Formular zur Weiterleitung
    except Exception as e:
        logging.error(f"Fehler beim Hochladen der Datei: {e}")
    try:

        return templates.TemplateResponse("video_duration.html", {
        "request": request,
        "file_name": file.filename,
        "file_location": file_location,
        "video_duration": video_duration,
        "duration": duration,
        "tags": tags
    })#return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

# Statische Dateien aus dem 'uploads' Verzeichnis bedienen
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Verzeichnis für Uploads erstellen, falls es nicht existiert
if not os.path.exists("uploads"):
    os.makedirs("uploads")
    

async def process_file(file_path: Path, filename: str):
    # Ensure that process_file can be called in a synchronous context
    tmp_file_path = FileManager.copy_to_tmp_directory(file_path, filename)
    Subtitle_gen.untertitel(tmp_file_path, filename)

# Determine the number of available CPUs and use all but one
max_workers = max(1, os.cpu_count() - 1)
executor = ProcessPoolExecutor(max_workers=max_workers)

app.mount("/videos", StaticFiles(directory="videos"), name="videos")

@app.post("/uploadfile/")
async def upload_file(request: Request, file_location: str = Form(...), video_duration: float = Form(...), duration: float = Form(...), tags: str = Form(...)):
    
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from file import FileManager
    from design import ProgramDesign
    from subtitle_gen import Subtitle_gen
    from db import DB

    # Sicherstellen, dass das Upload-Verzeichnis existiert
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    # Dateiort und Namen extrahieren
    file_path = Path(file_location)
    file_name = file_path.name
    filename = FileManager.get_file_name(file_path)
    # Verarbeitung der Datei
    tmp_file_path = FileManager.copy_to_tmp_directory(file_path, filename)
    FileManager.delete_tmp_file(file_path)
    print(tmp_file_path)
    Subtitle_gen.untertitel(tmp_file_path, filename)
    output_file = 'videos/' +filename + '/' + filename + '_subtitle.mp4'
    subtitle = 'videos/' +filename + '/' + filename + '_subtitel.srt'
    file_path = 'videos/' +filename + '/' + filename + '.mp4'
    FileManager.combine_video_with_subtitle(file_path, subtitle, output_file)
    try:
        DB.insert_video(output_file, tags)
        print("Yes")
    except:
        folder = "/videos/" + file_name
        FileManager.delete_tmp_folder(folder)
        print("No")
    return RedirectResponse(url="/", status_code=303)

@app.get("/status", response_class=HTMLResponse)
async def status_page(request: Request):
    # Holen Sie den output_file aus der Sitzung
    output_file = Request.session.get('output_file')

    # Stellen Sie sicher, dass ein output_file vorhanden ist
    if output_file:
        file_location = Path(UPLOAD_DIRECTORY) / output_file

        # Simple HTML to display status
        html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Upload abgeschlossen</title>
            </head>
            <body>
                <h1>Upload abgeschlossen</h1>
                <a href="{file_location}">Klick hier, um die Datei herunterzuladen</a>
            </body>
            </html>
            """
        return HTMLResponse(content=html_content)
    else:
        # Handle the case where no output_file is available
        return HTMLResponse(content="<h1>Keine Datei hochgeladen</h1>")
    
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from subtitle_gen import Subtitle_gen
    from file import FileManager
    from design import ProgramDesign
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
