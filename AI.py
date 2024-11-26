import sys
import time
import traceback
from datetime import datetime, date, timedelta
from threading import Thread

from fuzzywuzzy import fuzz
from queue import Queue

from Vosk_voice_v3 import OnlineTranscriber
from GigaChat import chat
from SpeechVoice_Silero_vThread import speech
from Assistent_capabilities import action_controll

voiceString = OnlineTranscriber()

class Assistent:
    def __init__(self):
        """Настройки"""
        self.name = 'феликс' # Феноменально естевственный лексический интелект какогото свойства
        self.listen_time_const = timedelta(seconds=5) # Допустимый разрыв в слушаемом тексте

        """Флаги"""
        self.voice_enter = False # Статус обработки текста меняеться если появилось имя ассистента
        self.voice_write_status = False # Стату записи запроса, если он False время записи истекло
        self.voice_status = False # Статус готовности текста к передаче в нейросеть
        self.speech_status = True #
        # Статусы
        self.current_action = 'listen'

        """Хранилища передаваемых данных"""
        self.listen_text = str()  # Текст для распознавания
        self.last_time_voice = datetime.now() # Точка времени прослушки текста
        self.action_signal = [[],[]]
        self.action_list = {'speech': False}



    # Модуль обрабтки текущей ситуации при входном токене
    def start_action(self, enter_token):
        self.voice_enter = enter_token
        self.voice_write_status = True
        self.listen_text = str()
        # Если есть поток озвучки ставим его на паузу
        if self.action_list['speech']:
            self.action_list['speech'].pause()


    def function_controll(self, engin):

        print('function_controll ENGIN=', engin)
        if engin:
            print('function_controll 1=', engin)
            if engin['action'] == 'stop':
                print('function_controll 2=', engin)
                """
                Почему то блокирует всю работу
                """
                if self.action_list['speech']:
                    self.action_list['speech'].play_Permissions = False
                    self.action_list['speech'].audio_queue = Queue()
                    self.action_list['speech'].resume()
                    self.action_list['speech'] = False
        # Почему то не очищает входную точку за собой
        print('1ACTION=', self.voice_enter)
        self.voice_enter = False
        print('2ACTION=', self.voice_enter)

    def enter_dot_v2(self, text):
        '''
        Получаем текст, разбиваем на токены
        если один из токенов имя ассистента то возвращаем номер токена
        номер токена являеться входной точкой с которой будет начинаться запрос

        :param text:
        :return:
        '''
        tokens = text.split()
        for n, token in enumerate(tokens):
            if fuzz.ratio(self.name, token) > 80:
                # print('TOKEN=', token, fuzz.ratio(self.name, token))
                return n
        return False

    def listen(self):
        '''
        Получаем ответы от слушаюшего скрипта в по сути бесконечном цикле


        Текст отдаеться на распознание соответствие имени Ассистента

        1. Текст делиться на токены если в тексте содержиться токен имени ассистента
        переменная self.voice_enter переходит в статус True

        2.Если статус прослушки текста активен мы начинаем его записывать /Добавить обработку функций/

        3. Если запись началась запускаем контроль времени на разрыв между вводами распознаваниями
        как только разрыв больше чем значение self.listen_time_const останавливаем запись и даем сигнал на вывод

        :return:
        '''


        # Штамп времени последнего расслышанного слова

        # Цикл получения текста распознавания

        def time_test():
            print('TIMER START')
            while True:
                print('TIMER=', datetime.now() - self.last_time_voice > self.listen_time_const)
                if datetime.now() - self.last_time_voice > self.listen_time_const:
                    if self.action_list['speech']:
                        self.action_list['speech'].resume()
                    self.voice_write_status = False
                    self.voice_status = True
                    break
                time.sleep(1)


        for text in voiceString.listen():
            try:
                enter_token = self.enter_dot_v2(text['Partial'])
                # Если токен действия найден, входной токен еще не существует или не равен текущему(новый)
                print(enter_token, self.voice_enter, enter_token)
                if enter_token is not False and self.voice_enter is False or self.voice_enter != enter_token:
                    print('-=TOKEN STAR=-')
                    self.start_action(enter_token) # Функция обработки момента точки входа
                    self.last_time_voice = datetime.now()
                    TIMER = Thread(target=time_test)
                    TIMER.start()
                # Если это не точка обновления текста из первого условия и при этом токен уже существует
                """elif self.voice_enter:
                    action_controll(text['Partial'], self.voice_enter)"""

                if self.voice_enter and self.voice_write_status:
                    self.last_time_voice = datetime.now()

            except:
                # print(traceback.print_exc())
                pass

            try:
                speech_flag = True
                # По сути проверка входного токена не требуется
                if (self.voice_enter or self.voice_enter == 0 and self.voice_enter is not False and
                        self.voice_write_status): # 0 равно False
                    print('TEXT INPUT=', text['Text'])
                    action_search = action_controll.search_fuction(text['Text'], self.voice_enter)
                    print(action_search)
                    for answer in action_search:
                        print(answer)
                        if answer:
                            # Функция проверки действия
                            speech_flag = False
                            self.function_controll(answer)

                    if speech_flag:
                        self.listen_text += text['Text']
                        self.last_time_voice = datetime.now()
            except:
                pass

    def speech(self):
        while True:
            if self.voice_status:
                text = ' '.join(self.listen_text.split()[self.voice_enter+1:])
                print('CHAT TEXT=', text)
                self.listen_text = ''
                self.voice_enter = False
                self.voice_status = False
                answer = chat.get_answer(text)
                self.action_list['speech'] = speech
                speech.play_Permissions = True
                speeching = Thread(target=speech.speak_sentences, args=(answer, 'text'))
                speeching.start()
                speeching.join()
                self.action_list['speech'] = False
            time.sleep(3)

    def start(self):
        listen = Thread(target=self.listen)
        speech = Thread(target=self.speech)

        listen.start()
        speech.start()


assistent = Assistent()
assistent.start()
