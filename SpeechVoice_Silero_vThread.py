import sounddevice as sd
import numpy as np
from queue import Queue
from threading import Event, Thread
import torch
from NLP import Text_spliter

class Speech:
    def __init__(self, generate_device='cpu'):
        self.device = torch.device(generate_device)
        self.threads_sum = 4
        self.local_file = 'C:\\P\\Python\\voice_model\\Silero\\v4_ru.pt'
        self.model = torch.package.PackageImporter(self.local_file).load_pickle("tts_models", "model")
        self.model.to(self.device)
        self.sample_rate = 48000
        self.speaker = 'eugene'
        torch.set_num_threads(self.threads_sum)

        self.audio_queue = Queue()
        self.pause_event = Event()  # Событие для управления паузой
        self.pause_event.set()  # Устанавливаем в состояние "разрешено"
        self.stream = None

    def voiceover(self):
        while True:
            audio_data = self.audio_queue.get()
            if audio_data is None:
                break

            # Воспроизводим аудио с использованием OutputStream
            self.stream = sd.OutputStream(samplerate=self.sample_rate, channels=1, callback=self.audio_callback)
            self.stream.start()

            # Запускаем воспроизведение
            self.audio_buffer = audio_data
            self.current_position = 0

            while self.current_position < len(self.audio_buffer):
                self.pause_event.wait()  # Ожидание, пока не будет разрешено продолжение
                sd.sleep(10)  # Небольшая задержка для избежания излишней загрузки процессора

            self.stream.stop()
            self.audio_queue.task_done()

    def audio_callback(self, outdata, frames, time, status):
        if status:
            print(status)
        # Проверяем состояние паузы
        if not self.pause_event.is_set():
            outdata.fill(0)  # Если пауза, заполняем выходные данные нулями
        else:
            # Заполняем выходные данные аудиобуфером
            chunk = self.audio_buffer[self.current_position:self.current_position + frames]
            outdata[:len(chunk)] = chunk.reshape(-1, 1)
            self.current_position += len(chunk)

    def generate_sample(self, text, text_type):
        if text_type == 'ssml':
            audio_tensor = self.model.apply_tts(ssml_text=text, speaker=self.speaker, sample_rate=self.sample_rate)
        else:
            audio_tensor = self.model.apply_tts(text=text, speaker=self.speaker, sample_rate=self.sample_rate)
        audio_data = audio_tensor.squeeze().cpu().numpy()
        return audio_data

    def speak_sentences(self, text, text_type: str, speed=3):
        playback_thread = Thread(target=self.voiceover)
        playback_thread.start()

        # Генерация аудиоданных
        if text_type == 'ssml':
            sentences = self.text_drober_ssml(text, speed)
        elif text_type == 'text':
            sentences = Text_spliter(text).proposal_list_optimized(minimal_token=10)
        else:
            raise ValueError(f'text_type wait ssml or text not {text_type}')
        for sentence in sentences:
            audio_data = self.generate_sample(sentence, text_type)
            if audio_data is not None:
                self.audio_queue.put(audio_data)

        self.audio_queue.put(None)
        playback_thread.join()

    def pause(self):
        self.pause_event.clear()  # Останавливаем воспроизведение

    def resume(self):
        self.pause_event.set()  # Возобновляем воспроизведение


# Пример использования
if __name__ == '__main__':
    text = 'Ваш текст для воспроизведения'
    speech = Speech()
    t = Thread(target=speech.speak_sentences, args=(text, 'text'))
    t.start()

    while True:
        command = input('pause/resume: ')
        if command == 'pause':
            speech.pause()
        elif command == 'resume':
            speech.resume()






