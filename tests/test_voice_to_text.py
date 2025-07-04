import pytest
from unittest.mock import patch, MagicMock
from modules.voice_to_text import VoiceToText


def test_voice_recognition():
    with patch('speech_recognition.Recognizer') as mock_recognizer, \
            patch('speech_recognition.AudioFile') as mock_audio:
        mock_audio_instance = MagicMock()
        mock_audio.return_value.__enter__.return_value = mock_audio_instance

        mock_rec_instance = MagicMock()
        mock_rec_instance.recognize_google.return_value = "test text"
        mock_recognizer.return_value = mock_rec_instance

        vtt = VoiceToText()
        result = vtt.transcribe_audio("test.wav")

        assert result == "test text"