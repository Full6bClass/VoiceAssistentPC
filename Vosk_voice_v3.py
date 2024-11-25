import vosk
import sys
import sounddevice as sd
import queue
import json
import os
import numpy as np
from scipy.fft import fft


class OnlineTranscriber:

    def __init__(self, model = 'voice_model/vosk/model_small', device = 1, audio_queue_size = 20, blocksize = 4000):

        # Установка модели
        self.model_path = os.path.join(os.getcwd(), *model.split('/'))
        self.model = vosk.Model(self.model_path)

        self.samplerate = 16000 # Дискретная частота для распознования vosk на тестах другие не работают хотя
        # хватило бы 8000

        self.device = device  # Устройство захвата аудио, установка номера девайса для ввода звука

        # Размер для очереди звука
        self.audio_queue_size = audio_queue_size

        # Увеличиваем размер блока данных
        self.blocksize = blocksize  # Размер блока в байтах (увеличенный)

        # Очередь для распознавания
        self.audio_queue = queue.Queue(maxsize=self.audio_queue_size)

        # Функция для обработки звукового потока
    def q_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        try:
            # Если очередь заполнена, пропускаем кадр
            self.audio_queue.put(bytes(indata), block=False)
        except queue.Full:
            print("Warning: Audio queue is full; dropping frames.")

    # Получение характеристик аудио
    def get_audio_features(self, data, samplerate):
        audio_data = np.frombuffer(data, dtype=np.int16)
        frequencies = fft(audio_data)
        power = np.abs(frequencies) ** 2
        return {
            "frequencies": frequencies[:len(frequencies) // 2],
            "power": power[:len(power) // 2]
        }

    def listen(self):
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=self.blocksize, device=self.device, dtype='int16', channels=1,
                               callback=self.q_callback):
            rec = vosk.KaldiRecognizer(self.model, self.samplerate)

            while True:
                try:
                    # Получаем данные из очереди
                    data = self.audio_queue.get()

                    # Подаем данные в распознаватель
                    if rec.AcceptWaveform(data):
                        # Получаем итоговый результат и аудиофичи
                        result = json.loads(rec.Result())
                        text = result.get("text", "")
                        if text:
                            features = self.get_audio_features(data, self.samplerate)
                            yield {"Text": text}
                            rec = vosk.KaldiRecognizer(self.model, self.samplerate)

                    else:
                        # Получаем частичный результат
                        partial_result = json.loads(rec.PartialResult())
                        partial_text = partial_result.get("partial", "")
                        if partial_text:
                            features = self.get_audio_features(data, self.samplerate)
                            yield {"Partial": partial_text} # , "Frequencies": features['frequencies'], "Power": features['power']}
                            # print(f"Partial Frequencies: {features['frequencies']}")
                            # print(f"Partial Power: {features['power']}")

                    # Очищаем переменные после обработки, чтобы освободить память
                    del data

                except queue.Empty:
                    pass  # Ждем новые данные, если очередь пуста


if __name__ == '__main__':
    voiceString = OnlineTranscriber()
    for row in voiceString.listen():
        try:
            print('PArt=', row['Partial'])
        except:
            pass
        try:
            print('Text=', row['Text'])
        except:
            pass
"""
voiceString = OnlineTranscriber()

for row in voiceString.listen():
    try:
        print(row['Text'])
    except:
        pass"""
