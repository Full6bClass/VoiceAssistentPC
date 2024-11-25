import sys
import time
import traceback
from datetime import datetime, date, timedelta
from threading import Thread

from fuzzywuzzy import fuzz

from Vosk_voice_v3 import OnlineTranscriber
from GigaChat import chat
from SpeechVoice_Silero_vThread import speech
from Assistent_capabilities import action_controll

voiceString = OnlineTranscriber()

class Assistent:
    def __init__(self):
        """Настройки"""
        self.name = 'феликс' # Феноменально естевственный лексический интелект какогото свойства
        self.listen_time_const = timedelta(seconds=3) # Допустимый разрыв в слушаемом тексте

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


    def action_test(self, enter_token, text):
        self.voice_enter = enter_token
        self.voice_write_status = True
        self.listen_text = str()
        print(self.action_list['speech'])
        if self.action_list['speech']:
            self.action_list['speech'].pause()




    def enter_dot(self, text):
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
                self.voice_enter = n
                self.voice_write_status = True
                return True

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
                print('TOKEN=', token, fuzz.ratio(self.name, token))
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
                if datetime.now() - self.last_time_voice > self.listen_time_const:
                    if self.action_list['speech']:
                        self.action_list['speech'].resume()
                    self.voice_write_status = False
                    self.voice_status = True
                    break
                time.sleep(1)

        TIMER = Thread(target=time_test)
        for text in voiceString.listen():
            try:
                """Тут нужно раздробить на деление функций получение токена для текста и функции
                if self.voice_enter == False:
                    searched = self.enter_dot(text['Partial'])
                    if searched:
                        self.last_time_voice = datetime.now()
                        TIMER.start()
                        
                if self.voice_enter and self.voice_write_status:
                    self.last_time_voice = datetime.now()
                """
                enter_token = self.enter_dot_v2(text['Partial'])
                if enter_token or enter_token == 0 and enter_token is not False:
                    print('TEXT PARTIAL=', text['Partial'])
                    print(enter_token)
                    self.action_test(enter_token, text['Partial'])
                    self.last_time_voice = datetime.now()
                    TIMER.start()

                if self.voice_enter and self.voice_write_status:
                    self.last_time_voice = datetime.now()

            except:
                # print(traceback.print_exc())
                pass

            try:
                if (self.voice_enter or self.voice_enter == 0 and self.voice_enter is not False and
                        self.voice_write_status): # 0 равно False
                    self.listen_text += text['Text']
                    self.last_time_voice = datetime.now()
            except:
                pass

    def speech(self):
        while True:
            print(0)
            print(self.voice_status)
            if self.voice_status:
                print('voice_enter=', self.voice_enter)
                print('listen_text=', self.listen_text)
                print(self.listen_text.split()[self.voice_enter+1:])
                text = ' '.join(self.listen_text.split()[self.voice_enter+1:])
                print('---TEXT=', text)
                """answer = chat.get_answer(text)
                self.action_list['speech'] = chat
                speeching = Thread(target=speech.speak_sentences, args=(answer, 'text'))
                t = [speeching]
                speeching.start()
                self.listen_text = ''
                self.voice_enter = False
                self.voice_status = False
                for s in t:
                    s.join()
                    self.action_list['speech'] = False"""
            time.sleep(3)

    def start(self):
        listen = Thread(target=self.listen)
        speech = Thread(target=self.speech)

        listen.start()
        speech.start()


assistent = Assistent()
assistent.start()

"""        for row in voiceString.listen():
            try:
                answer = chat.get_answer(row['Text'])
                if answer == False:
                  answer = 'Не понял ваш вопрос, не могли бы вы его повторить?'
                print(answer.replace('"', ''))
                sys.exit(0)
            except:
                pass"""