import requests
import json
from config import key, accaunt_key
import uuid

class Chat:
    def __init__(self, accaunt_key):
        self.accaunt_key = accaunt_key
        self.key = self.get_key()
        self.cert = 'cert.cer'

    def get_key(self):
        '''
        Инструкция на дэбаг:
        1.Установить верное время синхронизировав с интернет.
        2. Сертификат МИН цифры
        3. RqUID запроса

        :return:
        '''

        # Генерация уникального идентификатора запроса
        rq_uid = str(uuid.uuid4())

        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        # Путь к вашему сертификату

        cert_path = 'cert.cer'  # Укажите путь к вашему сертификату

        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': f'Basic {self.accaunt_key}',
            'RqUID': rq_uid
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=cert_path)
        return response.json()['access_token']

    def chat_single(self, text):
        print(1)
        print('CHAT ASK=', text)
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        payload = json.dumps({
          "model": "GigaChat",
          "messages": [
            {
              "role": "user",
              "content": text
            }
          ],
          "stream": False,
          "repetition_penalty": 1
        })
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': f'Bearer {self.key}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=self.cert)
        print(response)
        print(response.json())
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            self.key = self.get_key()
            return self.chat_single(text=text)

    def ask_stable(self, text):
        print(2)
        ask = self.chat_single(promts(keys=['ask_stable'], value=text))
        print('ASK in STABLE=', ask)
        if ask:
            return ask.replace('"', '')
        else:
            False

    def get_answer(self, text):
        print(0)
        print('GET ASK=', type(text), text)
        ask_stable = self.ask_stable(text)
        return self.chat_single(promts(keys=[], value=ask_stable))



def promts(keys: list, value):
    text = '[ask_stable] [text] [ask_speech_stable]'
    key_list = ['ask_stable', 'ask_speech_stable']
    promt = {
        'ask_stable':

            f'Я плохо расслышал что мне сказали попробуй исправить и напиши исправленный текст, '
            f'Пожалуйста, напишите ответ в формате Текст=[ваш исправленный текст]., вот что я услышал: ',


        'ask_speech_stable':

            ('В тексте ответа используй разметку для озвучки вот список элементов которые можно применить:'
            '<break time="">: пауза (например, 500ms максимум 1000ms); атрибут strength (x-weak, weak, medium, strong, x-strong).'
            '<prosody pitch="...">: изменение высоты (x-low, low, medium, high, x-high).'
            '<p>: параграф (эквивалент сильной паузе).'
            'в ответе должен быть только размечанный текст.')
    }

    #< s >: предложение(эквивалент очень сильной паузе). \
    # <speak>: корневой тег.
    for key in keys:
        text = text.replace(f'[{key}]', promt[key])
    for keyc in key_list:
        text = text.replace(f'[{keyc}]', '')

    text = text.replace('[text]', value)
    return text



if __name__ == 'GigaChat':
    chat = Chat(accaunt_key)

if __name__ == '__main__':
    chat = Chat(key['access_token'])
    print(chat.get_answer('Куда жене пригласить меня погулять'))









