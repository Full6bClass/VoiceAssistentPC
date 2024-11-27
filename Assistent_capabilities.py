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


class Action_controll:

    def __init__(self):
        self.action_box = {}


    def action_list(self):
        """
        На данный момент структура хранимых функций:
        [Функция, тип передаваемых данных, единаразовое действие или долгосрочная функция]
        1. передается экземпляр функции
        2. Тип данных если 0 то входные данные не требуются
        3. Если функция вроде включить/выключить звук не требующая дальнейшего контроля то 0
        если функция вроде браузера и будет работать в потоке то возвращаеться имя ключа в пуле потоков

        :return:
        """
        return {
                'стоп': 'stop',
                'остановись': 'stop',
                'звук': {
                    # Звук тише
                    ('убавить', 'уменьшить', 'снизь', 'приубавь', 'приглуши', 'тише'): [pc_action.volume_down, 'INTEGER', 0],

                    # Звук громче
                    ('прибавить', 'увеличить', 'повысить', 'усилить', 'поднять'): 'voice_high',

                        }
                }

    def action_list_v2(self):
        """
        На данный момент структура хранимых функций:
        [Функция, тип передаваемых данных, единаразовое действие или долгосрочная функция]
        1. передается экземпляр функции
        2. Тип данных если 0 то входные данные не требуются
        3. Если функция вроде включить/выключить звук не требующая дальнейшего контроля то 0
        если функция вроде браузера и будет работать в потоке то возвращаеться имя ключа в пуле потоков

        :return:
        """
        return {
                'стоп': 'stop',
                'остановись': 'stop',
                'звук': {
                    # Звук тише
                    'убавить': [pc_action.volume_down, 'INTEGER', 0],
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
        """
        Еще не реализована функция сохранения экземпляров класса для тех кто этого требует
        :param engin:
        :return:
        """
        # Определяем тип данных которые ищем
        # Если нужны числовые данные
        if engin['action'][1] == 'INTEGER':
            # Переводим в тексте данные в числа
            text = text_stable.words_to_numbers(engin['text'])
            # Ищем первый вход после токенов активаторов функции
            for token in text.split()[max(engin['chain']):]:
                try:
                    return int(token)
                except:
                    pass

    # Запускаем команду
    def action_start(self, engin):
        # Стабилизатор текста выдает значение передаваемое в функции в зависимости от её типа
        value = self.text_stable(engin)
        if value:
            engin['action'][0](value)
        else:
            engin['action'][0]()

    def search_fuction(self, text, enter_token):
        '''

        :param text:
        :param enter_token:
        :return:
        '''
        print('search_fuction=', text, enter_token)
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
                    yield {**result, 'text': text}
                else:
                    # Если функция это какая то реальная функция то запускаем её работу
                    self.action_start({**result, 'text': text})
                    yield True
                # searche_actions['action'].append(result)
                # searche_actions['chain'].append(parent_chain)
            else:
                break

        # Нужно или обрабатывать тут функции и запоминать потоки или вернуть обратно для записи их существование
        # Если исполняемые на моменте то нечего

    def search_fuction_v2(self, text, enter_token):
        '''

        :param text:
        :param enter_token:
        :return:
        '''
        print('search_fuction=', text, enter_token)
        # Разбираем текст на токены
        tokens = text.split()[enter_token:]
        text = ' '.join(tokens)
        # Это у нас список действий
        all_action_list = self.action_list_v2()
        searche_actions = {'action': [], 'chain': []}
        # Ищем токены в предложении
        for _ in range(0, len(tokens)):
            # Для сбора токенов по которым найдено
            parent_chain = []

            # Ищет функции
            def token_search(action_list):
                rait_engin = {'key': str(), 'rait': 0}

                # Перебираем сравнение токенов с ключами
                for key_input in action_list.keys():
                    if type(key_input) == tuple:
                        for key in key_input:
                            for token in tokens:
                                rait = fuzz.ratio(key, token)
                                # Находим лучший рейтинг
                                if rait > 70 and rait > rait_engin['rait']:
                                    rait_engin['key'], rait_engin['rait'] = key, rait
                    else:
                        key = key_input
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
                    yield {**result, 'text': text}
                else:
                    # Если функция это какая то реальная функция то запускаем её работу
                    self.action_start({**result, 'text': text})
                    yield True
                # searche_actions['action'].append(result)
                # searche_actions['chain'].append(parent_chain)
            else:
                break

        # Нужно или обрабатывать тут функции и запоминать потоки или вернуть обратно для записи их существование
        # Если исполняемые на моменте то нечего


if __name__ == '__main__':
    pc_action = PC_action()
    action_controll = Action_controll()

    for row in action_controll.search_fuction('кошка', 0):
        print(row)

if __name__ == 'Assistent_capabilities':
    pc_action = PC_action()
    action_controll = Action_controll()


"""
Список вункций
1. Удалить историю браузера
2.Открытие ссылок
3.Работа с сйтами
3.1. Работа с видео

"""
