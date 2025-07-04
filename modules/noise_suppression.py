import numpy as np
from scipy import signal
import logging


class NoiseSuppressor:
    def __init__(self):
        self.logger = logging.getLogger("NoiseSuppressor")

    def apply(self, audio_data: np.array, sample_rate: int) -> np.array:
        try:
            b, a = signal.butter(4, 1000, 'lowpass', fs=sample_rate)
            filtered = signal.filtfilt(b, a, audio_data)
            self.logger.info("Шумоподавление применено")
            return filtered
        except Exception as e:
            self.logger.error(f"Ошибка: {str(e)}")
            return audio_data