import bcrypt
import os
import sys
from db import Db

src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

class User:
    @staticmethod
    def register_user(username, password):
        # Retrieve the salt from the database or generate one if not present
        salt = Db.get_user_salt(username)
        
        if not salt:
            # If the salt doesn't exist, generate a new one
            salt = bcrypt.gensalt()

        # Wenn der Salt bereits ein bytes-Objekt ist, muss er nicht konvertiert werden
        if isinstance(salt, str):
            salt = salt.encode('utf-8')

        # Hash the password using the retrieved or generated salt
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        
        # Store the hashed password and salt in the database
        info = Db.register_user(username, hashed_password.decode('utf-8'), salt.decode('utf-8'))
        return info

    @staticmethod
    def authenticate_user(username, password):
        # Retrieve the stored password hash and salt from the database
        myresult = Db.login_user(username)
        
        if myresult:
            stored_password = myresult['password'].encode('utf-8')
            salt = myresult['salt'].encode('utf-8')

            # Hash the input password using the retrieved salt
            hashed_password = bcrypt.hashpw(password.encode(), salt)
            
            # Compare the hashed input password with the stored password
            if hashed_password == stored_password:
                return True
            else:
                return False
        else:
            return None  # Return None if no result is found

