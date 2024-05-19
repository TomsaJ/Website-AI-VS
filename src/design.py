class ProgramDesign:
    def __init__(self):
        self.github = "LauriTrite und TomsaJ"
        self.repo = "https://github.com/TomsaJ/Projekt-KI-Untertitel.git"
        self.version = "1.3"
        self.description = "Erstellt mit whisper einen Untertitel für das\nausgewählte Video und verbindet beides miteinander"
        ProgramDesign.print_info(self)

    def print_info(self):
        ProgramDesign.lines()
        print("                     Videos mit Untertitel")
        ProgramDesign.lines()
        print(f"Autor: {self.github}")
        print(f"Version: {self.version}")
        print(f"Github: {self.github}")
        print(f"Repo: {self.repo}")
        print(f"Beschreibung: {self.description}")
        ProgramDesign.lines()
        ProgramDesign.lines()
    
    def duration(video_duration, d):
        print(f"Dauert: {(video_duration * d)/60:.2f} Minuten")

    def neededtime(execution_time):
        print("Der Untertitel wurde in {:.2f} Minuten erzeugt.".format((execution_time/60)%60))

    def lines():
        print("=" * 65)

if __name__ == "__main__":
    info = ProgramDesign(
        author="Max Mustermann",
        version="1.0",
        description="Eine coole Anwendung, die alles kann!"
    )
