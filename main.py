import sys
import subprocess
import importlib.util
import time
import os


# Herausfinden, auf welchem Betriebssystem die Anwendung läuft
current_os = os.name

PATH_SEPARATOR = ''

if current_os == 'nt':  # nt bedeutet Windows
    PATH_SEPARATOR = '\\'
else:  # posix bedeutet Unix/Linux/MacOS
    PATH_SEPARATOR = '/'

def install_packages():
    packages = [
        "fastapi",
        "starlette",
        "uvicorn",
        "aiofiles",
        "jinja2",
        "fastapi-sessions"
        #"cupy"
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
from starlette.config import Config
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)
from html_design import HTML
from subtitle_gen import Subtitle_gen
from file import FileManager
from db import DB
from design import ProgramDesign
#import cupy as cp

# Configure session secret
config = Config('.env')
SECRET_KEY = config('SECRET_KEY', cast=str, default='your-secret-key')

app = FastAPI() 
logging.basicConfig(level=logging.INFO)
app.add_middleware(SessionMiddleware, secret_key="some-random-secret-key")
# Verzeichnis zum Speichern der hochgeladenen Dateien
UPLOAD_DIRECTORY = "uploads"
# Stelle sicher, dass das Upload-Verzeichnis existiert
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="page")
# Determine the number of available CPUs and use all but one
max_workers = max(1, os.cpu_count() - 1)
executor = ProcessPoolExecutor(max_workers=max_workers)
app.mount("/videos", StaticFiles(directory="videos"), name="videos")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

def timeout(request):
    time_request = request.session.get('time')
    thirty_m = 3 * 60
    current_time = int(time.time())
    tmp = current_time-time_request
    print(tmp)
    print (thirty_m)
    if(tmp < thirty_m):
        refresh(request)
        return
    else:
        request.session.clear()
        return

def refresh(request):
    request.session['time'] = int(time.time())
    return

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from db import DB
    import time
    current_time = time.time()
    time = int(current_time)
    DB.delete_Video(time)
    logged_in = False
    username = request.session.get('user')
    if username:
        user =  username
        logged_in = True
        timeout(request)
    else:
        user= "Noch niemand angemeldet"  
    header = HTML.header(logged_in)
    footer = HTML.foot(username)
    try:
        videos_html = "<p>"+ "Hallo" + "</p>"
        return templates.TemplateResponse("index.html", {"request": request, "videos": videos_html, "user": user, "foot":footer, "header": header})
        #return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

@app.get("/about", response_class=HTMLResponse)
async def main_page(request: Request):
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from db import DB
    import time
    current_time = time.time()
    time = int(current_time)
    DB.delete_Video(time)
    logged_in = False
    username = request.session.get('user')
    if username:
        user =  username
        logged_in = True
        timeout(request)
    else:
        user= "Noch niemand angemeldet"  
    header = HTML.header(logged_in)
    footer = HTML.foot(username)
    script = HTML.foot_script()
    try:
        videos_html = "<p>"+ "Hallo" + "</p>"
        return templates.TemplateResponse("about.html", {"request": request, "script": script, "user": user, "foot":footer, "header": header})
        #return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)


@app.get("/upload/", response_class=HTMLResponse)
async def upload_page(request: Request):
    logged_in = False
    username = request.session.get('user')
    if username:
        logged_in = True
    header = HTML.header(logged_in)
    footer = HTML.foot(username)
    try:
        src_path = os.path.join(os.path.dirname(__file__), 'src')
        sys.path.append(src_path)
        from db import DB
        username = request.session.get('user')
        lang = DB.all_lang()
        
        return templates.TemplateResponse("upload.html", {"request": request, "lang": lang, "user": username, "foot":footer, "header": header})
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

# Route, um die Datei zu empfangen und zu verarbeiten
@app.post("/upload_duration/", response_class=HTMLResponse)
async def upload_duration(request: Request, file: UploadFile = File(...), lang: str = Form(...), user: str = Form(...)):
    # Importieren der Module
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from file import FileManager
    from design import ProgramDesign
    import time
    print(lang)
    current_time = time.time()
    logged_in = False
    username = request.session.get('user')
    if username:
        logged_in = True
    header = HTML.header(logged_in)
    footer = HTML.foot(username)
    try:
        # Sicherstellen, dass das Upload-Verzeichnis existiert
        upload_dir = UPLOAD_DIRECTORY
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Zeitstempel zum Dateinamen hinzufügen
        timestamp = str(int(current_time))
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]
        new_filename = f"{os.path.splitext(original_filename)[0]}_{timestamp}{file_extension}"
        
        # Dateipfad erstellen
        file_location = os.path.join(upload_dir, new_filename)
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
        "lang": lang,
        "user": user,
        "time": timestamp,
        "foot":footer, "header": header
    })#return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

# Statische Dateien aus dem 'uploads' Verzeichnis bedienen

# Verzeichnis für Uploads erstellen, falls es nicht existiert
if not os.path.exists("uploads"):
    os.makedirs("uploads")
    
@app.post("/uploadfile/")
async def upload_file(request: Request, file_location: str = Form(...), video_duration: float = Form(...), duration: float = Form(...), lang: str = Form(...), user: str = Form(...), time: str= Form(...)):
    
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
    #Subtitle_gen.untertitel(tmp_file_path, filename, lang, use_gpu=True)
    Subtitle_gen.untertitel(tmp_file_path, filename, lang)
    output_file = 'videos' + PATH_SEPARATOR +filename + PATH_SEPARATOR + filename + '_subtitle.mp4'
    subtitle = 'videos' + PATH_SEPARATOR +filename + PATH_SEPARATOR + filename + '_subtitle.srt'
    file_path = 'videos' + PATH_SEPARATOR +filename + PATH_SEPARATOR + filename + '.mp4'
    lang = DB.get_language_code(lang)
    FileManager.combine_video_with_subtitle(file_path, subtitle, output_file, lang)
    folder = "videos" + PATH_SEPARATOR + filename+ PATH_SEPARATOR
    try:
        DB.insert_video(output_file, user, folder, time)
        print("Yes")
        request.session['output_file'] = output_file 
    except:
        folder = PATH_SEPARATOR +"videos"+PATH_SEPARATOR + file_name
        FileManager.delete_tmp_folder(folder)
        print("No")
    return RedirectResponse(url="/me", status_code=303)
    
@app.get("/login", response_class=HTMLResponse)
async def upload_page(request: Request):
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from html_design import HTML
    logged_in = False
    username = request.session.get('user')
    if username:
        logged_in = True
    header = HTML.header(logged_in)
    footer = HTML.foot(username)
    try:
        return templates.TemplateResponse("login.html", {"request": request,  "foot":footer, "header": header})
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)


@app.post("/login-check")
async def login(request: Request, username: str =  Form(...), password: str = Form(...)):
    if DB.login(username, password):
        request.session['user'] = username
        request.session['time'] = int(time.time())

# Print the stored timestamp
        print(request.session['time'])
        return RedirectResponse(url="/me", status_code=303)
    else:
        raise HTTPException(status_code=401, detail="Ungültige Anmeldeinformationen")

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/me", response_class=HTMLResponse)
async def upload_page(request: Request):
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from db import DB
    from html_design import HTML
    username = request.session.get('user')
    video = DB.videos(username)
    username = request.session.get('user')
    logged_in = False
    if username:
        user = "Willkomen, "
        user +=  username
        logged_in = True
    else:
        user = '''<h2>Melde dich bitte an!</h2><br>
<button onclick="window.location.href='/login'">Anmelden</button>'''
    header = HTML.header(logged_in)
    footer = HTML.foot(username)
    try:
        if logged_in:
            return templates.TemplateResponse("me.html", {"request": request, "foot":footer, "user": user, "video": video, "header": header})
        else: return templates.TemplateResponse("me.html", {"request": request, "foot":footer, "user": user, "video": "",  "header": header})
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

    
if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from subtitle_gen import Subtitle_gen
    from file import FileManager
    from db import DB
    from design import ProgramDesign
    from html_design import HTML
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=30000)
