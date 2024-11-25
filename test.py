# from seleniumwire import webdriver
from fuzzywuzzy import fuzz
import os

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from NLP import text_stable





class PC_action:

    def volume_down(self, step):
        if step > 10:
            step = step / 100
        elif 0 >= step > 100:
            step = 1
        # Получаем все аудиовыходы
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Получаем текущую громкость
        current_volume = volume.GetMasterVolumeLevelScalar()

        # Уменьшаем громкость на заданное количество единиц
        new_volume = max(0.0, current_volume - step)

        # Устанавливаем новую громкость
        volume.SetMasterVolumeLevelScalar(new_volume, None)

class Browser:
    def __init__(self):
        self.driver = self.Driver()

    def Driver(self):

        # service = Service(ChromeDriverManager().install())

        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(r'user-data-dir={}\WbSession\{}'.format(os.getcwd(), self.user_id))
        options.add_argument('--profile-directory=Profile 1')
        options.add_argument("--no-sandbox")
        options.add_argument("--remote-debugging-pipe")
        # options.add_argument("--headless")
        # from selenium.webdriver.chrome.service import Service

        # service = Service(executable_path='C:/path/to/chromedriver.exe')
        # Создаем сервис для ChromeDriver
        return webdriver.Chrome(options=options) #, service=service)

    def open_yandex(self):
        self.driver.get('yandex.ru')

# pc_action = PC_action()
class Action_controll:
    print(1)
    def action_list(self):
        return {
                'стоп': 'stop',
                'звук': {
                    # Звук тише
                    'убавить': '',
                    'уменьшить': [pc_action.volume_down, 'INTEGER'],
                    'снизь': [pc_action.volume_down, 'INTEGER'],
                    'приубавь': [pc_action.volume_down, 'INTEGER'],
                    'приглуши': [pc_action.volume_down, 'INTEGER'],
                    'тише': [pc_action.volume_down, 'INTEGER'],
                    # Звук громче
                    'прибавить': 'voice_high',
                    'увеличить': 'voice_high',
                    'повысить': 'voice_high',
                    'усилить': 'voice_high',
                    'поднять': 'voice_high',

                        }
                }
    def text_stable(self, engin):
        if engin['action']['type_value'] == 'INTEGER':
            enter_dot = False
            text = text_stable.words_to_numbers(engin['text'])
            for token in text.split():
                if enter_dot is False:
                    if token == engin['chain'][-1]:
                        enter_dot = True
                else:
                    try:
                        return int(token)
                    except:
                        pass


    def action_start(self, engin):
        print(engin)
        value = self.text_stable(engin)
        print('VALUE=',value)
        if value:
            engin['action'](value)


    def enter_knot(self, text, enter_token):
        '''

        :param text:
        :param enter_token:
        :return:
        '''
        # Разбираем текст на токены
        tokens = text.split()[enter_token:]
        text = ' '.join(tokens)
        # Это у нас список действий
        all_action_list = self.action_list()
        searche_actions = {'action': [], 'chain': []}
        # Ищем токены в предложении
        for _ in range(0, len(tokens)):
            # Для сбора токенов по которым найдено
            parent_chain = []
            # Ищет функции
            def token_search(action_list):
                rait_engin = {'key': str(), 'rait': 0}
                # Перебираем сравнение токенов с ключами
                for key in action_list.keys():
                    for token in tokens:
                        rait = fuzz.ratio(key, token)
                        # Находим лучший рейтинг
                        if rait > 70 and rait > rait_engin['rait']:
                            rait_engin['key'], rait_engin['rait'] = key, rait
                # Если нашли нужные ключи
                if rait_engin['rait'] != 0:
                    # Вытаскиваем индекс токена подошедшего
                    index = tokens.index(rait_engin['key'])
                    # Индекс заменятьеся на 0 что бы сохранить порядок но убрать повторение значения
                    tokens[index] = '0'
                    # В найденные пишем индекс в строке токена
                    parent_chain.append(index)
                    # Записываем функцию токена
                    result = action_list[rait_engin['key']]
                    # Если результат это словарь то ищем в нем
                    if type(result) == dict:
                        return token_search(result)
                    else:
                        return {'action': result, 'chain': parent_chain}
                else:
                    return False
            # Получаем найденную функцию и её создателей
            result = token_search(action_list=all_action_list)
            # Если функция найдена
            if result is not False:
                # Если функция строка отправляем запроснику для обработки
                if type(result['action']) == str:
                    yield {'action': result, 'chain': parent_chain, 'text': text}
                else:
                    # Если функция это какая то реальная функция то запускаем её работу
                    self.action_start({'action': result, 'text': text})
                searche_actions['action'].append(result)
                searche_actions['chain'].append(parent_chain)
            else:
                break
        # Нужно или обрабатывать тут функции и запоминать потоки или вернуть обратно для записи их существование
        # Если исполняемые на моменте то нечего


if __name__ == '__main__':
    action = Action_controll()
    f = action.enter_knot('убавить стоп звук', 0)
    for row in f:
        print(row)
