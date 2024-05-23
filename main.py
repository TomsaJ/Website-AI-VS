from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
import shutil
import os
import sys
from pathlib import Path

app = FastAPI()

# Verzeichnis zum Speichern der hochgeladenen Dateien
UPLOAD_DIRECTORY = "uploads"

# Stelle sicher, dass das Upload-Verzeichnis existiert
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def main():
    with open("index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.post("/uploadfile/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    file_location = Path(UPLOAD_DIRECTORY) / file.filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_path= file_location
    background_tasks.add_task(process_file, file_path, file.filename)
    
    return {"info": f"Datei '{file.filename}' erfolgreich hochgeladen"}

async def process_file(file_path: Path, filename: str):
    tmp_file_path = FileManager.copy_to_tmp_directory(file_path, filename)
    Subtitle_gen.untertitel(tmp_file_path, filename)

if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from subtitle_gen import Subtitle_gen
    from file import FileManager
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
