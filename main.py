from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
import shutil
import os
import sys
import aiofiles
import logging
from fastapi.staticfiles import StaticFiles
from concurrent.futures import ProcessPoolExecutor

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Verzeichnis zum Speichern der hochgeladenen Dateien
UPLOAD_DIRECTORY = "uploads"

# Stelle sicher, dass das Upload-Verzeichnis existiert
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def main_page():
    try:
        async with aiofiles.open("page/index.php", "r") as file:
            content = await file.read()
            return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

@app.get("/upload/", response_class=HTMLResponse)
async def upload_page():
    try:
        async with aiofiles.open("page/upload.php", "r") as file:
            content = await file.read()
            return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

# Route, um die Datei zu empfangen und zu verarbeiten
@app.post("/upload_duration/", response_class=HTMLResponse)
async def upload_duration(file: UploadFile = File(...)):
    # Importieren der Module
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from file import FileManager
    from design import ProgramDesign
    
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
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload abgeschlossen</title>
        </head>
        <body>
            <h1>Upload abgeschlossen</h1>
            <p>Datei: {file.filename}</p>
            <p>Speicherort: {file_location}</p>
            <p>Video Dauer: {video_duration}</p>
            <p>Berechnete Dauer: {duration}</p>
            <form action="/uploadfile/" method="post" enctype="multipart/form-data">
                <input type="hidden" name="file" value="{file.filename}">
                <input type="hidden" name="file_location" value="{file_location}">
                <input type="hidden" name="video_duration" value="{video_duration}">
                <input type="hidden" name="duration" value="{duration}">
                <input type="submit" value="Bestätigen und fortfahren">
            </form>
            <script>
                document.getElementById('hiddenForm').submit();
            </script>
        </body>
        </html>
        """

        return HTMLResponse(content=content)

    except Exception as e:
        logging.error(f"Fehler beim Hochladen der Datei: {e}")
        return HTMLResponse(content="Fehler beim Hochladen der Datei", status_code=500)

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

@app.post("/uploadfile/")
async def upload_file(file_location: str = Form(...), video_duration: float = Form(...), duration: float = Form(...)):
    
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from file import FileManager
    from design import ProgramDesign
    from subtitle_gen import Subtitle_gen

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
    FileManager.combine_video_with_subtitle(file_path, subtitle, output_file)
    
    # Redirect to a status page
    return RedirectResponse(url=f"/status/{filename}", status_code=303)


@app.get("/status/{filename}", response_class=HTMLResponse)
async def status_page(request: Request, filename: str):
    file_location = Path(UPLOAD_DIRECTORY) / filename
    
    # Simple HTML to display status
    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload abgeschlossen</title>
        </head>
        <body>
            <h1>Upload abgeschlossen</h1>
            
        </body>
        </html>
        """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from subtitle_gen import Subtitle_gen
    from file import FileManager
    from design import ProgramDesign
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
