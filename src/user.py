from db import Db

srcpath = os.path.join(os.path.dirname(_file), 'src')
sys.path.append(src_path)

class User:
    def register_user(username, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        info = Db.register_user(username, password)
        return info
    def authenticate_user(username, password):
        myresult = Db.login_user(username, password)
        password = hashlib.sha256(password.encode()).hexdigest()
        if myresult:
            stored_password = myresult[0]
            if password == stored_password:
                return True
            else:
                return False
        else:
            return None  # return None, wenn kein Ergebnis gefunden wurde