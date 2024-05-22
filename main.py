from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import shutil
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
async def upload_file(file: UploadFile = File(...)):
    file_location = Path(UPLOAD_DIRECTORY) / file.filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"Datei '{file.filename}' erfolgreich hochgeladen"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
