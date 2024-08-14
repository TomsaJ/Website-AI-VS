import unittest
import bcrypt
from user import User
from unittest.mock import patch

class TestUserAuthentication(unittest.TestCase):

    @patch('db.Db.get_user_salt')
    @patch('db.Db.register_user')
    @patch('db.Db.login_user')
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

    @patch('db.Db.get_user_salt')
    @patch('db.Db.login_user')
    def test_authenticate_user(self, mock_login_user, mock_get_user_salt):
        username = "admin"
        password = "admin"
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        
        # Simulate the return of the salt and hashed password from the database
        mock_get_user_salt.return_value = salt.decode('utf-8')
        mock_login_user.return_value = {'password': hashed_password.decode('utf-8'), 'salt': salt.decode('utf-8')}
        
        # Test user authentication
        result = User.authenticate_user(username, password)
        
        self.assertTrue(result)
        mock_login_user.assert_called_once()

if __name__ == '__main__':
    unittest.main()
