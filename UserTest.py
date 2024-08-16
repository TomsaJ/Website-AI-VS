import unittest
import bcrypt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from user import User
from db import Db
from unittest.mock import patch

class TestUserAuthentication(unittest.TestCase):

    @patch('src.db.Db.register_user')
    @patch('src.db.Db.login_user')
    def test_register_user(self, mock_login_user, mock_register_user):
        # Simulate a Salt value that would be returned by the database
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
        data = password, "admin"
        mock_login_user.return_value = data
        # Test user authentication
        result = User.authenticate_user(username, password)
        self.assertEqual(result, "admin")
        mock_login_user.assert_called_once_with(username)

    @patch('src.db.Db.login_user')
    def test_authenticate_user_failed(self, mock_login_user):
        username = "admin"
        password = "admin"
        salt = User.generate_salt()
        password = User.hash_password(password, salt)
        password = salt.decode('utf-8') + password.decode('utf-8')
        data = password, "admin"
        mock_login_user.return_value = data
        # Test user authentication
        result = User.authenticate_user(username, "password")
        print (result)
        self.assertEqual(result, False)
        mock_login_user.assert_called_once_with(username)

if __name__ == '__main__':
    unittest.main()
