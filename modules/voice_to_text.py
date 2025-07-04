import speech_recognition as sr
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class VoiceToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            logging.info("✅ Микрофон доступен")
        except Exception as e:
            logging.error(f"❌ Микрофон недоступен: {e}")
            self.microphone = None

    def transcribe_audio(self, file_path):
        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language="ru-RU")
                logging.info(f"🔊 Распознано: {text}")
                return text
        except sr.UnknownValueError:
            logging.error("❌ Речь не распознана (неразборчиво или тихо)")
        except Exception as e:
            logging.error(f"❌ Ошибка при обработке файла: {e}")
        return None


if __name__ == "__main__":
    vtt = VoiceToText()

    result = vtt.transcribe_audio("test_audio.wav")
    if result:
        print("✅ Результат:", result)
    else:
        print("❌ Не удалось распознать речь")