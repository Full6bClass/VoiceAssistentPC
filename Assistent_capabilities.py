from seleniumwire import webdriver
from fuzzywuzzy import fuzz
import os

class PC_action:

    def voice_control(self):
        pass

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


def action_controll(text):
    action = {'стоп': 'stop'}

    key_list = ['стоп']
    for key in key_list:
        if fuzz.partial_ratio(key, text) > 70:
            return action[key]

    '''
    Тут будет передаваться текст для выявления действия

    Если не найдено действие возвращаем ничего
    :return:
    '''
    return False

"""
Список вункций
1. Удалить историю браузера
2.Открытие ссылок
3.Работа с сйтами
3.1. Работа с видео

"""
