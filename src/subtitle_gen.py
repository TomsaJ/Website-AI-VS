import asyncio
import whisper
import datetime
import torch
import os

class Subtitle_gen:
    @staticmethod
    def untertitel(file_path, filename):
        #if torch.cuda.is_available():
        #    device = "cuda"
        #elif torch.backends.mps.is_available():
        #    device = "mps"
        #else:
        #    device = "cpu"
        device = "cpu"
        model = whisper.load_model("medium", device=device)
        options = whisper.DecodingOptions(language='de', fp16=False)
        result = model.transcribe(file_path)
        
        # Speichern der SRT-Datei
        save_target_srt = os.path.join(os.getcwd(), filename + '_subtitel.srt')
        with open(save_target_srt, 'w') as file:
            for indx, segment in enumerate(result['segments'], start=1):
                start_time = datetime.timedelta(seconds=segment['start'])
                end_time = datetime.timedelta(seconds=segment['end'])
                start_hours = start_time.seconds // 3600
                start_minutes = (start_time.seconds % 3600) // 60
                start_seconds = start_time.seconds % 60
                end_hours = end_time.seconds // 3600
                end_minutes = (end_time.seconds % 3600) // 60
                end_seconds = end_time.seconds % 60
                start_time_str = f"{start_hours:02}:{start_minutes:02}:{start_seconds:02},{start_time.microseconds // 1000:03}"
                end_time_str = f"{end_hours:02}:{end_minutes:02}:{end_seconds:02},{end_time.microseconds // 1000:03}"
                file.write(str(indx) + '\n')
                file.write(start_time_str + ' --> ' + end_time_str + '\n')
                file.write(segment['text'].strip() + '\n\n')
        
        # Speichern der Textdatei
        save_target_txt = os.path.join(os.getcwd(), filename + '_videotext.txt')
        with open(save_target_txt, 'w') as file:
            file.write(result['text'])
        with open(save_target_txt, 'w') as file:
            for indx, segment in enumerate(result['segments'], start=1):
                text = segment['text'].strip()
                # Überprüfe, ob der Text ein Punkt enthält
                if '.' in text:
                    text += '\n'  # Füge einen Zeilenumbruch hinzu
                file.write(text)