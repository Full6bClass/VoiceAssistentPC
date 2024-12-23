import time

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

class Browser:
    def __init__(self):
        self.user_id = 'test'
        self.driver = False


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
        self.driver.get('https://ya.ru/')

    def yandex_search(self, text):
        if self.driver is False:
            self.driver = self.Driver()
        self.open_yandex()

        # Ожидание загрузки input по частичному совпадению класса
        search_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class*='search3__input']"))
        )
        search_input.click()

        # Ввод текста в input
        search_input.send_keys(text)  # Замените на нужный текст

        # Ожидание загрузки кнопки по частичному совпадению класса
        search_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='search3__button']"))
        )
        search_button.click()