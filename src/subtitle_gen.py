import asyncio
import whisper
import datetime
import os

class Subtitle_gen:
    @staticmethod
    async def untertitel(file_path, filename):
        model = whisper.load_model("medium")
        options = whisper.DecodingOptions(language='de', fp16=False)
        result = model.transcribe(file_path)
        save_target = os.path.join(os.getcwd(), filename, filename + '_subtitel.srt')
        # Öffnen der SRT-Datei zum Schreiben
        with open(save_target, 'w') as file:
            # Schleife über die Untertitelabschnitte
            for indx, segment in enumerate(result['segments'], start=1):
                # Konvertiere Start- und Endzeit in einen String im gewünschten Format mit Komma für Dezimalstellen und drei Dezimalstellen für die Millisekunden
                start_time = datetime.timedelta(seconds=segment['start'])
                end_time = datetime.timedelta(seconds=segment['end'])
                # Extrahiere Stunden, Minuten und Sekunden
                start_hours = start_time.seconds // 3600
                start_minutes = (start_time.seconds % 3600) // 60
                start_seconds = start_time.seconds % 60
                end_hours = end_time.seconds // 3600
                end_minutes = (end_time.seconds % 3600) // 60
                end_seconds = end_time.seconds % 60
                # Konstruiere den Zeitstempel im gewünschten SRT-Format
                start_time_str = f"{start_hours:02}:{start_minutes:02}:{start_seconds:02},{start_time.microseconds // 1000:03}"
                end_time_str = f"{end_hours:02}:{end_minutes:02}:{end_seconds:02},{end_time.microseconds // 1000:03}"
                # Schreiben der Zeitangaben und des Textes des Untertitels in die SRT-Datei
                file.write(str(indx) + '\n')
                file.write(start_time_str + ' --> ' + end_time_str + '\n')
                file.write(segment['text'].strip() + '\n\n')
        save_target = os.path.join(os.getcwd(), filename, filename +'_videotext.txt')
        with open(save_target, 'w') as file:
            for indx, segment in enumerate(result['segments'], start=1):
                text = segment['text'].strip()
                # Überprüfe, ob der Text ein Punkt enthält
                if '.' in text:
                    text += '\n'  # Füge einen Zeilenumbruch hinzu
                file.write(text)