import datetime
import os
import re
import torch

from NLP import Text_spliter, text_stable
from datetime import datetime

import numpy as np
import sounddevice as sd
from threading import Thread
from queue import Queue

from typing import Literal


class Speech:
    def __init__(self, generate_device='cpu'):
        self.device = torch.device(generate_device)
        self.threads_sum = 4
        self.local_file = str(os.getcwd()) + "/voice_model/Silero/" + 'v4_ru.pt'
        self.model = torch.package.PackageImporter(self.local_file).load_pickle("tts_models", "model")
        self.model.to(self.device)
        self.sample_rate = 48000
        self.speaker = 'eugene'  # aidar, baya, kseniya, xenia, eugene, random
        torch.set_num_threads(self.threads_sum)

        self.audio_queue = Queue()  # Очередь для хранения сгенерированных аудиоданных


    def voice_speed(self, speed=3):
        return {1:  'x-slow', 2: 'slow', 3: 'medium', 4: 'fast', 5: 'x-fast'}[speed]

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
            # Удаление лишних тегов и пробелов
            sentence = f'<speak><prosody rate="{self.voice_speed(speed)}">' + sentence.strip() + '</prosody></speak>'
            if sentence and re.search(r'<speak><prosody rate=".+"></prosody></speak>',
                                      sentence) is None:  # Проверка, что предложение не пустое
                text_complete.append(sentence)

        return text_complete

    def text_drober_naked(self, text):
        tokens = text.split(' ')
        tokens_len = len(tokens)
        result = []
        if tokens_len > 20:
            parts = text.split('\n')
            for part in parts:
                part_token = part.split()
                if len(part_token) > 20:
                    result.extend([t for t in part.split('.') if t])
                elif len(part_token) < 5:
                    if part:
                        result[-1] += part
                else:
                    result.append(part)
        else:
            result = [text]
        return result

    def generate_sample(self, text, text_type):
        # Применение метода apply_tts для генерации речи
        if text_type == 'ssml':
            audio_tensor = self.model.apply_tts(ssml_text=text, speaker=self.speaker, sample_rate=self.sample_rate)
        else:
            audio_tensor = self.model.apply_tts(text=text, speaker=self.speaker, sample_rate=self.sample_rate)
        audio_data = audio_tensor.squeeze().cpu().numpy()
        return audio_data

    def voiceover(self):
        while True:
            audio_data = self.audio_queue.get()  # Получение аудиоданных из очереди
            if audio_data is None:  # Проверка на завершение
                break
            sd.play(audio_data, self.sample_rate)
            sd.wait()  # Ожидание завершения воспроизведения
            self.audio_queue.task_done()  # Уведомление о завершении обработки

    def speak_sentences(self, text, text_type: Literal['ssml', 'text'], speed=3):
        print('INPUT TEXT SPEAKER=', text)
        # Запуск потока для воспроизведения аудио
        playback_thread = Thread(target=self.voiceover)
        playback_thread.start()

        if text_type == 'ssml':
            # Разделение текста на предложения
            sentences = self.text_drober_ssml(text, speed)
        elif text_type == 'text':
            sentences = Text_spliter(text).proposal_list_optimized(minimal_token=10)
        else:
            raise ValueError(f'text_type wait ssml or text not {text_type}')

        for sentence in sentences:
            print(f"Генерация: {sentence}")  # Для отладки
            t1 = datetime.now()
            audio_data = self.generate_sample(text_stable.numbers_to_words(sentence), text_type)

            if audio_data is not None:
                self.audio_queue.put(audio_data)  # Добавление аудиоданных в очередь
            t2 = datetime.now()
            print(t2-t1)

        self.audio_queue.put(None)  # Отправка сигнала завершения
        playback_thread.join()  # Ожидание завершения потока воспроизведения


# Пример использования
if __name__ == "SpeechVoice_Silero":
    speech = Speech()

if __name__ == '__main__':

    speech = Speech()
    text = ('Для того чтобы сделать сухарики со вкусом сыра, используют технологию ароматизации продукта. Сырный вкус достигается за счет добавления специальных пищевых добавок – ароматизаторов, которые имитируют вкус сыра. Вот несколько основных этапов этого процесса:'
'### 1. Выбор основы'
   'В качестве основы для сухарей чаще всего используется хлеб или батон. Хлеб нарезают на небольшие кусочки, которые затем обжаривают или сушат до хрустящего состояния.'
'### 2. Приготовление сухарей'
   'Нарезанные кусочки хлеба высушиваются при низкой температуре (около 100–120°C), пока они не станут полностью сухими и хрустящими. Этот процесс может занимать от нескольких минут до часа в зависимости от толщины кусочков.'
'### 3. Добавление масла'
   'После сушки сухари могут быть слегка смазаны растительным маслом. Это помогает ароматизатору лучше распределиться по поверхности сухаря.'
'### 4. Использование ароматизатора'
   'Ароматизаторы могут быть натуральными или искусственными. Натуральные ароматизаторы изготавливаются из экстрактов настоящего сыра, тогда как искусственные – из химических соединений, которые точно воспроизводят сырный вкус.'
   'На этом этапе сухари смешиваются с порошковым ароматизатором, который равномерно распределяется по их поверхности. Важно соблюдать правильную дозировку, чтобы вкус был насыщенным, но не слишком резким.'
'### 5. Охлаждение и упаковк'
  'Сухари охлаждают до комнатной температуры и упаковывают в герметичные пакеты, чтобы сохранить свежесть и предотвратить потерю аромата.'
'Таким образом, главное отличие заключается в использовании специального ароматизатора, который придает продукту нужный вкус без необходимости добавлять сам сыр.')

    print(speech.speak_sentences(text, text_type='text'))

