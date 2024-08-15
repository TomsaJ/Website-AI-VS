import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from file import FileManager
from db import Db  # Adjust the import based on your actual file structure

class TestDb(unittest.TestCase):

    def test_sanitize_input(self):
        # Test data
        input_str = "username; DROP TABLE users;"
        expected_output = "username DROP TABLE users"

        # Call the method
        result = Db.sanitize_input(input_str)

        # Assertion
        self.assertEqual(result, expected_output)

    @patch('mysql.connector.connect')
    @patch('os.getenv')
    def test_db_conn_success(self, mock_getenv, mock_connect):
        # Mock the environment variables
        mock_getenv.side_effect = lambda var_name, default: {
            "DB_HOST": "localhost",
            "DB_USER": "admin",
            "DB_PASSWORD": "admin",
            "DB_NAME": "WS-AI-VS"
        }.get(var_name, default)

        # Mock the connection behavior
        mock_connection = MagicMock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection

        # Call the method
        connection = Db.db_conn()

        # Assertions
        self.assertIsNotNone(connection)
        mock_connect.assert_called_once()

    @patch('mysql.connector.connect')
    def test_db_conn_failure(self, mock_connect):
        # Mock connection to raise an error
        mock_connect.side_effect = Error("Connection failed")

        # Call the method
        connection = Db.db_conn()

        # Assertion
        self.assertIsNone(connection)

    @patch('mysql.connector.connect')
    def test_get_user_salt(self, mock_connect):
        # Mock the connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('somesalt',)
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection

        # Call the method
        salt = Db.get_user_salt('testuser')

        # Assertions
        self.assertEqual(salt, 'somesalt')
        mock_cursor.execute.assert_called_once_with("SELECT salt FROM user WHERE username = %s", ('testuser',))

    @patch('mysql.connector.connect')
    def test_insert_video(self, mock_connect):
        # Mock the connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Call the method
        Db.insert_video('/path/to/video.mp4', 'testuser', 'folder', 1234567890)

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO videos (path, user, folder, time) VALUES (%s, %s, %s, %s)",
            ('/path/to/video.mp4', 'testuser', 'folder', 1234567890)
        )
        mock_connection.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_get_videos(self, mock_connect):
        # Mock the connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('/path/to/video1.mp4', '/folder1/'),
            ('/path/to/video2.mp4', '/folder2/')
        ]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Mock FileManager.get_file_name
        with patch.object(FileManager, 'get_file_name', side_effect=lambda x: os.path.basename(x).split('.')[0]):
            # Call the method
            result = Db.get_videos('testuser')

            # Assertions
            self.assertIn('<video width="320" height="270" controls>', result)
            self.assertIn('<source src="/path/to/video1.mp4" type="video/mp4">', result)
            self.assertIn('<source src="/path/to/video2.mp4" type="video/mp4">', result)

    @patch('mysql.connector.connect')
    def test_get_all_lang(self, mock_connect):
        # Mock the connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('english',), ('spanish',)]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Call the method
        result = Db.get_all_lang()

        # Assertions
        self.assertIn('<option value="English">English</option>', result)
        self.assertIn('<option value="Spanish">Spanish</option>', result)

    @patch('mysql.connector.connect')
    def test_get_language_code(self, mock_connect):
        # Mock the connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('en',)
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Call the method
        code = Db.get_language_code('english')

        # Assertions
        self.assertEqual(code, 'en')
        mock_cursor.execute.assert_called_once_with(
            "SELECT language_code FROM language WHERE language_name = %s",
            ('english',)
        )

    @patch('mysql.connector.connect')
    def test_register_user(self, mock_connect):
        # Mock the connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Call the method
        result = Db.register_user('testuser', 'hashedpassword')

        # Assertions
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO user (username, password) VALUES (%s, %s)",
            ('testuser', 'hashedpassword')
        )
        mock_connection.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_login_user(self, mock_connect):
        # Mock the connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('hashedpassword', 'testuser')
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Call the method
        result = Db.login_user('testuser')

        # Assertions
        self.assertEqual(result, ('hashedpassword', 'testuser'))
        mock_cursor.execute.assert_called_once_with(
            "SELECT password, username FROM user WHERE username = %s",
            ('testuser',)
        )

    @patch('mysql.connector.connect')
    @patch('os.path.isdir')
    @patch('shutil.rmtree')
    def test_delete_video(self, mock_rmtree, mock_isdir, mock_connect):
        # Mock the connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, '/path/to/folder1', 1000000000),
            (2, '/path/to/folder2', 2000000000)
        ]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        mock_isdir.return_value = True

        # Call the method
        Db.delete_video(3000000000)

        # Assertions
        mock_cursor.execute.assert_any_call("DELETE FROM videos WHERE id = %s", (1,))
        mock_connection.commit.assert_any_call()
        mock_rmtree.assert_any_call('/path/to/folder1')

if __name__ == '__main__':
    unittest.main()
