import os
import sys
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

from installPackage import PackageInstaller
from moviepy.editor import VideoFileClip
from subtitle_gen import Subtitle_gen
from file import FileManager
from timer import Time
from installation import Installation
from design import ProgramDesign

json_file_path = "src/data.json"

app = FastAPI()

# Serve the static HTML file
app.mount("/static", StaticFiles(directory="static"), name="static")

if not os.path.exists(json_file_path):
    Installation.startup()

PackageInstaller.check_and_install_package('openai-whisper')
PackageInstaller.check_and_install_package('ffmpeg-python')
PackageInstaller.check_and_install_package('moviepy')


async def subtitel(file_path, filename):
    sub = Subtitle_gen()
    await sub.untertitel(file_path, filename)


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(('.mp4', '.mkv', '.avi')):
            raise HTTPException(status_code=400, detail="Invalid file format. Only .mp4, .mkv, .avi files are accepted.")
        
        filename = FileManager.get_file_name(file.filename)
        file_path = os.path.join("/tmp", filename)
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Optional: You can add subtitle generation logic here if needed.
        
        return JSONResponse(status_code=200, content={
            "message": "File uploaded successfully",
            "file_path": file_path
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
