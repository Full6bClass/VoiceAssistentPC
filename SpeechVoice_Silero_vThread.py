import os

import sounddevice as sd
import numpy as np
from queue import Queue
from threading import Event, Thread
import torch
from NLP import Text_spliter

class Speech:
    def __init__(self, generate_device='cpu'):
        self.play_Permissions = True
        self.device = torch.device(generate_device)
        self.threads_sum = 4
        self.local_file = os.getcwd() + '\\voice_model\\Silero\\v4_ru.pt'
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
    text = 'Жил-был в одном маленьком городке человек по имени Алексей. Он был простым работником на местной фабрике, где производили игрушки для детей. Каждый день Алексей вставал рано утром, завтракал овсянкой с ягодами и отправлялся на работу. Несмотря на однообразие своей жизни, он всегда находил радость в мелочах. Алексей любил гулять по парку после работы. Он часто садился на скамейку и наблюдал за детьми, которые играли с игрушками, сделанными на его фабрике. Эти моменты приносили ему спокойствие и удовлетворение. Он мечтал о том, чтобы однажды создать свою собственную игрушку, которая бы радовала детей и приносила им счастье. Однажды, прогуливаясь по парку, Алексей заметил старую, заброшенную лавочку. Она была покрыта слоем краски и выглядела так, будто давно не видела рук человека. Вдохновившись, он решил восстановить эту лавочку и сделать её местом, где дети могли бы играть. Он собрал инструменты и начал работу. Каждый вечер после работы Алексей приходил в парк и восстанавливал лавочку. Он красил её в яркие цвета, добавлял рисунки и даже сделал небольшие столики для игр. Прошло несколько недель, и вскоре лавочка преобразилась. Дети начали собираться там, играя и смеясь. Алексей чувствовал себя счастливым, наблюдая за их радостью. Однажды к нему подошла мама одного из мальчиков и поблагодарила его за работу. Она рассказала, как её сын любит играть на этой лавочке и как это место стало для них особенным. Алексей был тронут её словами. Он понял, что его маленькое дело принесло радость не только ему, но и другим. С тех пор Алексей стал активнее участвовать в жизни своего городка. Он организовывал игры и конкурсы для детей, собирал игрушки и дарил их тем, кто в них нуждался. Его лавочка стала местом, где собирались не только дети, но и взрослые, которые делились своими историями и смеялись вместе. Так, благодаря своей настойчивости и любви к детям, Алексей нашел смысл в жизни и стал настоящим героем своего городка. Его история вдохновила многих, и вскоре в городе начались другие проекты, направленные на улучшение жизни людей. Алексей понял, что даже небольшие действия могут изменить мир к лучшему.'
    speech = Speech()
    t = Thread(target=speech.speak_sentences, args=(text, 'text'))
    t.start()

    while True:
        command = input('pause/resume: ')
        if command == 'pause':
            speech.pause()
        elif command == 'resume':
            speech.resume()

if __name__ == 'SpeechVoice_Silero_vThread':
    speech = Speech()




