import bcrypt
import os
import sys
from .db import Db

class User:
    @staticmethod
    def register_user(username, password, email):
        # Generate a new salt
        e = Db.check_email(email)
        a = Db.check_user(username)
        if (e):
            return "Vorhanden"
        if (a):
            return "UserVorhanden"
        salt = User.generate_salt()
        # Hash the password using the generated salt
        hashed_password = User.hash_password(password, salt)
        # Combine the salt and hashed password for storage
        hashed_password_with_salt = salt.decode('utf-8') + hashed_password.decode('utf-8')

        # Store the hashed password with salt in the database
        info = Db.register_user(username, hashed_password_with_salt, email)
        return "Erstellt"

    @staticmethod
    def authenticate_user(username, password):
        # Retrieve the stored password hash and salt from the database
        result = Db.login_user(username)
        
        if result:
            # Unpack the result tuple to get the stored hashed password
            stored_hashed_password_with_salt = result[0]
            # Extract salt from the stored password
            salt = stored_hashed_password_with_salt[:29].encode('utf-8')  # Extract the bcrypt salt, typically 29 chars
            # Generate hash of the input password using the extracted salt
            login_hash_password = User.hash_password(password, salt)
            login_hash_password_with_salt = salt.decode('utf-8') + login_hash_password.decode('utf-8')
            
            # Compare the hashed input password with the stored password
            if login_hash_password_with_salt == stored_hashed_password_with_salt:
                return True # Username
            else:
                return False
        else:
            return None  # Return None if no result is found

    @staticmethod
    def generate_salt():
    # Generate a salt using bcrypt
        salt = bcrypt.gensalt()
        return salt

    @staticmethod
    def hash_password(password, salt):
    # Hash the password with the provided salt using bcrypt
        salted_hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return salted_hash_password
