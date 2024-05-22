import os
import sys
import shutil
import time
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

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

if not os.path.exists(json_file_path):
    Installation.startup()

PackageInstaller.check_and_install_package('openai-whisper')
PackageInstaller.check_and_install_package('ffmpeg-python')
PackageInstaller.check_and_install_package('moviepy')


async def subtitel(file_path, filename):
    sub = Subtitle_gen()
    await sub.untertitel(file_path, filename)


@app.get("/")
async def root():
    return {"message": "Welcome to the Subtitle Generator API"}


@app.post("/generate_subtitle/")
async def generate_subtitle(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(('.mp4', '.mkv', '.avi')):
            raise HTTPException(status_code=400, detail="Invalid file format. Only .mp4, .mkv, .avi files are accepted.")
        
        upload_dir = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)  # Erstelle das Verzeichnis, falls es nicht existiert
        
        filename = FileManager.get_file_name(file.filename)
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        video_duration = FileManager.duration_video(file_path)
        d = FileManager.readjson()
        ProgramDesign.duration(video_duration, d)
        
        start_time = time.time()
        await subtitel(file_path, filename)
        end_time = time.time()
        execution_time = end_time - start_time
        
        output_file = os.path.join(upload_dir, filename + '_subtitle.mp4')
        subtitle = os.path.join(upload_dir, filename + '_subtitel.srt')
        FileManager.combine_video_with_subtitle(file_path, subtitle, output_file)
        
        FileManager.delete_tmp_file(file_path)
        FileManager.move_tmp_directory_back(file_path, filename)
        
        ProgramDesign.neededtime(execution_time)
        
        return JSONResponse(status_code=200, content={
            "message": "Subtitle generated successfully",
            "output_file": output_file,
            "execution_time": execution_time
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
