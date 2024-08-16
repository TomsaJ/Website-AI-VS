from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import logging
import time
import shutil

from .html_design import Html
from .subtitle_gen import SubtitleGen
from .file import FileManager
from .db import Db
from .design import ProgramDesign
from .user import User

router = APIRouter()

templates = Jinja2Templates(directory="page")
UPLOAD_DIRECTORY = "uploads"
PATH_SEPARATOR = '\\' if os.name == 'nt' else '/'

@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    current_time = time.time()
    time_int = int(current_time)
    Db.delete_video(time_int)
    logged_in = False
    username = request.session.get('user')
    if username:
        logged_in = True
        timeout(request)
    user = username if username else "Noch niemand angemeldet"  
    header = Html.header(logged_in)
    footer = Html.foot(username)
    try:
        videos_html = "<p>"+ "Hallo" + "</p>"
        return templates.TemplateResponse("index.html", {"request": request, "videos": videos_html, "user": user, "foot":footer, "header": header})
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    current_time = time.time()
    time_int = int(current_time)
    Db.delete_video(time_int)
    logged_in = False
    username = request.session.get('user')
    if username:
        logged_in = True
        timeout(request)
    user = username if username else "Noch niemand angemeldet"  
    header = Html.header(logged_in)
    footer = Html.foot(username)
    script = Html.foot_script()
    try:
        return templates.TemplateResponse("about.html", {"request": request, "script": script, "user": user, "foot":footer, "header": header})
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

@router.get("/upload/", response_class=HTMLResponse)
async def upload_page(request: Request):
    logged_in = False
    username = request.session.get('user')
    if username:
        logged_in = True
    header = Html.header(logged_in)
    footer = Html.foot(username)
    try:
        lang = Db.get_all_lang()
        return templates.TemplateResponse("upload.html", {"request": request, "lang": lang, "user": username, "foot":footer, "header": header})
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

@router.post("/upload_duration/", response_class=HTMLResponse)
async def upload_duration(request: Request, file: UploadFile = File(...), lang: str = Form(...), user: str = Form(...)):
    current_time = time.time()
    logged_in = False
    username = request.session.get('user')
    if username:
        logged_in = True
    header = Html.header(logged_in)
    footer = Html.foot(username)
    try:
        upload_dir = UPLOAD_DIRECTORY
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        timestamp = int(current_time)
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]
        new_filename = f"{os.path.splitext(original_filename)[0]}_{timestamp}{file_extension}"
        
        file_location = os.path.join(upload_dir, new_filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        faktor = FileManager.readjson()
        video_duration = FileManager.duration_video(file_location)
        duration = ProgramDesign.duration(video_duration, faktor)
        print (faktor)
        print (duration)
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
        "timestamp": timestamp,
        "foot":footer, "header": header
    })
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

@router.post("/uploadfile/")
async def upload_file(request: Request, file_location: str = Form(...), video_duration: float = Form(...), duration: float = Form(...), lang: str = Form(...), user: str = Form(...), timestamp: int= Form(...)):
    start = time.time()
    file_path = Path(file_location)
    file_name = file_path.name
    filename = FileManager.get_file_name(file_path)
    tmp_file_path = FileManager.copy_to_tmp_directory(file_path, filename)
    FileManager.delete_tmp_file(file_path)
    print(tmp_file_path)
    SubtitleGen.create_subtitles(tmp_file_path, filename, lang, "medium")
    output_file = 'videos' + PATH_SEPARATOR +filename + PATH_SEPARATOR + filename + '_subtitle.mp4'
    subtitle = 'videos' + PATH_SEPARATOR +filename + PATH_SEPARATOR + filename + '_subtitle.srt'
    file_path = 'videos' + PATH_SEPARATOR +filename + PATH_SEPARATOR + filename + '.mp4'
    lang = Db.get_language_code(lang)
    FileManager.combine_video_with_subtitle(file_path, subtitle, output_file, lang)
    folder = "videos" + PATH_SEPARATOR + filename + PATH_SEPARATOR
    try:
        Db.insert_video(output_file, user, folder, timestamp)
        print("Yes")
        request.session['output_file'] = output_file 
        end = time.time()
        new_d = end-start
        Time.add_newtime(new_d , duration)
    except:
        folder = PATH_SEPARATOR +"videos"+PATH_SEPARATOR + filename
        FileManager.delete_tmp_folder(folder)
        print("No")
    return RedirectResponse(url="/me", status_code=303)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    logged_in = False
    username = request.session.get('user')
    if username:
        logged_in = True
    header = Html.header(logged_in)
    footer = Html.foot(username)
    try:
        return templates.TemplateResponse("login.html", {"request": request,  "foot":footer, "header": header})
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

@router.get("/reg", response_class=HTMLResponse)
async def reg_page(request: Request):
    logged_in = False
    username = request.session.get('user')
    if username:
        logged_in = True
    header = Html.header(logged_in)
    footer = Html.foot(username)
    try:
        return templates.TemplateResponse("reg.html", {"request": request,  "foot":footer, "header": header})
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

@router.post("/login-check")
async def login_check(request: Request, username: str =  Form(...), password: str = Form(...)):
    if User.authenticate_user(username, password):
        request.session['user'] = username
        request.session['time'] = int(time.time())
        print(request.session['time'])
        return RedirectResponse(url="/me", status_code=303)
    else:
        raise HTTPException(status_code=401, detail="Ungültige Anmeldeinformationen")

@router.post("/reg-check")
async def reg_check(request: Request, username: str =  Form(...), password: str = Form(...)):
    User.register_user(username, password)
    return RedirectResponse(url="/login", status_code=303)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@router.get("/me", response_class=HTMLResponse)
async def me_page(request: Request):
    username = request.session.get('user')
    video = Db.get_videos(username)
    logged_in = False
    if username:
        user = "Willkomen, " + username
        logged_in = True
    else:
        user = '''<h2>Melde dich bitte an!</h2><br>
<button onclick="window.location.href='/login'">Anmelden</button>'''
    header = Html.header(logged_in)
    footer = Html.foot(username)
    try:
        return templates.TemplateResponse("me.html", {"request": request, "foot":footer, "user": user, "video": video if logged_in else "", "header": header})
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)

def timeout(request):
    time_request = request.session.get('time')
    thirty_m = 3 * 60
    current_time = int(time.time())
    tmp = current_time - time_request
    print(tmp)
    print(thirty_m)
    if(tmp < thirty_m):
        refresh(request)
    else:
        request.session.clear()

def refresh(request):
    request.session['time'] = int(time.time())
