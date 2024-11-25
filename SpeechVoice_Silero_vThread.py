import datetime
import os
import re
import torch
# import numpy as np
import sounddevice as sd
from threading import Thread, Event
from queue import Queue
from typing import Literal
from NLP import Text_spliter, text_stable

class Speech:
    def __init__(self, generate_device='cpu'):
        self.device = torch.device(generate_device)
        self.threads_sum = 4
        self.local_file = str(os.getcwd()) + "/voice_model/Silero/" + 'v4_ru.pt'
        self.model = torch.package.PackageImporter(self.local_file).load_pickle("tts_models", "model")
        self.model.to(self.device)
        self.sample_rate = 48000
        self.speaker = 'eugene'
        torch.set_num_threads(self.threads_sum)

        self.audio_queue = Queue()
        self.pause_event = Event()  # Событие для управления паузой
        self.pause_event.set()  # Устанавливаем в состояние "разрешено"

    def voice_speed(self, speed=3):
        return {1: 'x-slow', 2: 'slow', 3: 'medium', 4: 'fast', 5: 'x-fast'}[speed]

    def text_drober_ssml(self, text, speed):
        parts = re.split(r'(<break time="\d+ms"/>)', text)
        text_l = []
        text_complete = []
        for i, row in enumerate(parts):
            if re.match('<break time="\d+ms"/>', row):
                text_l[-1] += row
            else:
                text_l.append(row)

        for sentence in text_l:
            sentence = f'<speak><prosody rate="{self.voice_speed(speed)}">' + sentence.strip() + '</prosody></speak>'
            if sentence and re.search(r'<speak><prosody rate=".+"></prosody></speak>', sentence) is None:
                text_complete.append(sentence)

        return text_complete

    def generate_sample(self, text, text_type):
        if text_type == 'ssml':
            audio_tensor = self.model.apply_tts(ssml_text=text, speaker=self.speaker, sample_rate=self.sample_rate)
        else:
            audio_tensor = self.model.apply_tts(text=text, speaker=self.speaker, sample_rate=self.sample_rate)
        audio_data = audio_tensor.squeeze().cpu().numpy()
        return audio_data

    def voiceover(self):
        while True:
            audio_data = self.audio_queue.get()
            if audio_data is None:
                break
            sd.play(audio_data, self.sample_rate)

            while sd.get_stream().active:  # Пока воспроизведение активно
                print('VOICE COVER=', self.pause_event)
                self.pause_event.wait()  # Ожидание, пока не будет разрешено продолжение

            self.audio_queue.task_done()

    def speak_sentences(self, text, text_type: Literal['ssml', 'text'], speed=3):
        playback_thread = Thread(target=self.voiceover)
        playback_thread.start()

        if text_type == 'ssml':
            sentences = self.text_drober_ssml(text, speed)
        elif text_type == 'text':
            sentences = Text_spliter(text).proposal_list_optimized(minimal_token=10)  # Здесь вы можете добавить свою логику для разбивки текста
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
if __name__ == "SpeechVoice_Silero_vThread":
    speech = Speech()
