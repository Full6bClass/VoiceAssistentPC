# from seleniumwire import webdriver
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


def action_controll(text, enter_token):
    # Разбираем текст на токены
    tokens = text.split()[enter_token:]
    # Это у нас список действий
    all_action_list = {
                'стоп': 'stop',
                'звук': {
                        'убавить': 'voice_low',
                        'прибавить': 'voice_high'
                        }
              }
    searche_actions = {'action': [], 'chain': []}
    for _ in range(0, len(tokens)):
        print(tokens)
        parent_chain = []
        def token_search(action_list):
            rait_engin = {'key': str(), 'rait': 0}
            for key in action_list.keys():
                for token in tokens:
                    rait = fuzz.ratio(key, token)
                    if rait > 70 and rait > rait_engin['rait']:
                        print(key, rait)
                        rait_engin['key'], rait_engin['rait'] = key, rait
            if rait_engin['rait'] != 0:
                parent_chain.append(rait_engin['key'])
                result = action_list[rait_engin['key']]
                if type(result) == dict:
                    return token_search(result)
                else:
                    return result
            else:
                return False

        tokens = [i for i in tokens if i not in parent_chain]
        result = token_search(action_list=all_action_list)
        if result is not False:
            searche_actions['action'].append(result)
            searche_actions['chain'].append(parent_chain)
        else:
            break

    return searche_actions


if __name__ == '__main__':

    test = action_controll('звук убавить, стоп', 0)
    print(test)

"""
Список вункций
1. Удалить историю браузера
2.Открытие ссылок
3.Работа с сйтами
3.1. Работа с видео

"""
