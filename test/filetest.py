import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import subprocess  # Import subprocess module
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from file import FileManager
# Assuming the FileManager class is in a file named file_manager.py

class TestFileManager(unittest.TestCase):

    @patch('os.makedirs')
    @patch('shutil.copy')
    @patch('os.path.basename')
    def test_copy_to_tmp_directory(self, mock_basename, mock_copy, mock_makedirs):
        # Setup mocks
        mock_basename.return_value = 'test_file.txt'
        mock_copy.return_value = None
        file_path = '/path/to/test_file.txt'
        filename = 'test_video'
        result = FileManager.copy_to_tmp_directory(file_path, filename)
        mock_makedirs.assert_called_once_with('videos/test_video', exist_ok=True)
        mock_basename.assert_called_once_with(file_path)
        mock_copy.assert_called_once_with(file_path, 'videos/test_video/test_file.txt')
        self.assertEqual(result, 'videos/test_video/test_file.txt')

    @patch('shutil.move')
    @patch('os.path.dirname')
    def test_move_tmp_directory_back(self, mock_dirname, mock_move):
        mock_dirname.return_value = '/destination/path'

        destination_path = '/destination/path/videos/test_video/test_file.txt'
        folder_name = 'test_video'

        result = FileManager.move_tmp_directory_back(destination_path, folder_name)

        mock_dirname.assert_called_once_with(destination_path)
        mock_move.assert_called_once_with(folder_name, '/destination/path/test_video')
        self.assertEqual(result, '/destination/path')

    @patch('shutil.rmtree')
    def test_delete_tmp_folder(self, mock_rmtree):

        folder_path = '/path/to/tmp_folder'

        FileManager.delete_tmp_folder(folder_path)

        mock_rmtree.assert_called_once_with(folder_path)

    @patch('os.remove')
    def test_delete_tmp_file(self, mock_remove):

        file_path = '/path/to/tmp_folder/file.txt'


        FileManager.delete_tmp_file(file_path)

        mock_remove.assert_called_once_with(file_path)

    def test_get_file_name(self):

        file_path = '/path/to/video.mp4'

        result = FileManager.get_file_name(file_path)

        self.assertEqual(result, 'video')

    @patch('subprocess.run')
    @patch('os.path.exists')
    def test_combine_video_with_subtitle(self, mock_exists, mock_run):

        mock_exists.side_effect = [True, True]
        mock_run.return_value = None

        # Test data
        video_file = 'video.mp4'
        subtitle_file = 'subtitle.srt'
        output_file = 'output.mp4'
        lang = 'en'

        FileManager.combine_video_with_subtitle(video_file, subtitle_file, output_file, lang)

        mock_exists.assert_any_call(video_file)
        mock_exists.assert_any_call(subtitle_file)
        mock_run.assert_called_once_with(
            [
                "ffmpeg", "-i", video_file, "-i", subtitle_file,
                "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text",
                "-map", "0:v:0", "-map", "0:a:0", "-map", "1:s:0",
                "-metadata:s:s:0", "language=" + lang, output_file
            ],
            stdout=subprocess.DEVNULL,  # Correcting the expected value
            stderr=subprocess.STDOUT
        )

    @patch('moviepy.editor.VideoFileClip')
    def test_duration_video(self, mock_video_clip):
        mock_clip_instance = MagicMock()
        mock_clip_instance.duration = 10.5
        mock_video_clip.return_value = mock_clip_instance

        video_file = 'video.mp4'

        result = FileManager.duration_video(video_file)

        mock_video_clip.assert_called_once_with(video_file)
        mock_clip_instance.close.assert_called_once()
        self.assertEqual(result, 10.5)


if __name__ == '__main__':
    unittest.main()
