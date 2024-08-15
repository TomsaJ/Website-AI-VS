import unittest
import bcrypt
import os
import sys


from src.user import User
from src.db import Db
from unittest.mock import patch

class TestUserAuthentication(unittest.TestCase):

    @patch('src.db.Db.get_user_salt')
    @patch('src.db.Db.register_user')
    @patch('src.db.Db.login_user')
    def test_register_user(self, mock_login_user, mock_register_user, mock_get_user_salt):
        # Simulate a Salt value that would be returned by the database
        mock_get_user_salt.return_value = None  # Salt doesn't exsist 
        mock_register_user.return_value = True  # Assume registration is successful

        username = "admin"
        password = "admin"
        
        # Test user registration
        result = User.register_user(username, password)
        self.assertTrue(result)
        mock_register_user.assert_called_once()

    @patch('src.db.Db.login_user')
    def test_authenticate_user(self, mock_login_user):
        username = "admin"
        password = "admin"

        salt = User.generate_salt()
        password = User.hash_password(password, salt)
        password = salt.decode('utf-8') + password.decode('utf-8')
        resulta = password, 'admin'
        mock_login_user.return_value = {resulta}
        # Test user authentication
        result = User.authenticate_user(username, password)
        
        self.assertEqual('admin' ,result)
        mock_login_user.assert_called_once()

if __name__ == '__main__':
    unittest.main()
