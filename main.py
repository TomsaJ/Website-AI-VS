from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

# Verzeichnis für hochgeladene Dateien
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB Limit

@app.route('/')
def index():
    return "Welcome to the File Upload API. Use the /upload endpoint to upload files."

@app.route('/upload', methods=['POST'])  # Nur POST-Anfragen erlauben
def upload_file():
    if request.method == 'POST':
        # Prüfen, ob die Anfrage eine Datei enthält
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        # Prüfen, ob eine Datei ausgewählt wurde
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Datei speichern
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return jsonify({"message": "File uploaded successfully", "file_path": file_path, "filename": filename}), 200
    else:
        return jsonify({"error": "Method not allowed"}), 405  # Falls eine andere Methode als POST verwendet wird

if __name__ == '__main__':
    app.run(debug=True)
