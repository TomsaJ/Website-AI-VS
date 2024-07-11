srcpath = os.path.join(os.path.dirname(_file), 'src')
sys.path.append(src_path)
from db import DB
class User:
    def registration(username, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        info = DB.registration(username, password)
        return info
    def login(username, password):
        myresult = DB.login(username, password)
        password = hashlib.sha256(password.encode()).hexdigest()
        if myresult:
            stored_password = myresult[0]
            if password == stored_password:
                return True
            else:
                return False
        else:
            return None  # Rückgabe None, wenn kein Ergebnis gefunden wurde