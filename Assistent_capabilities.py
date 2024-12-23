

from fuzzywuzzy import fuzz
import os
from action_tool.PC_action import Audio_control
from action_tool.Browser import Browser

from NLP import text_stable

audio_controll = Audio_control()







class Action_controll:

    def __init__(self):
        self.action_box = {}


    def action_list(self):
        print('list')
        """
        На данный момент структура хранимых функций:
        [Функция, тип передаваемых данных, единаразовое действие или долгосрочная функция]
        1. передается экземпляр функции
        2. Тип данных если 0 то входные данные не требуются
        3. Если функция вроде включить/выключить звук не требующая дальнейшего контроля то True
        если функция вроде браузера и будет работать в потоке то возвращаеться имя ключа в пуле потоков

        :return:
        """
        return {
                ('стоп', 'остановись'): 'stop',
                ('звук', 'громкость'): {
                    # Звук тише
                    ('убавить', 'уменьшить', 'снизь', 'приубавь', 'приглуши', 'тише', 'меньше'): [audio_controll.volume_down_step, 'INTEGER', True],

                    # Звук громче
                    ('прибавить', 'увеличить', 'повысить', 'усилить', 'поднять'): [audio_controll.volume_high_step, 'INTEGER', True],
                        },

                ('найди', 'найти'): [{'class': Browser, 'func': 'yandex_search', 'class_name': 'Browser'}, 'STRING', True],
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
            return False

        elif engin['action'][1] == 'STRING':
            # Переводим в тексте данные в числа
            # Ищем первый вход после токенов активаторов функции
            tokens = engin['text'].split()[max(engin['chain']) + 1:]
            if tokens:
                return " ".join(tokens)
            else:
                return False



    # Запускаем команду
    def action_start(self, engin):
        print(engin)
        # Стабилизатор текста выдает значение передаваемое в функции в зависимости от её типа
        value = self.text_stable(engin)
        try:
            engin_class = engin['action'][0]
            try:
                class_ = self.action_box[engin_class['class_name']]
                attr = getattr(class_(), engin_class['func'])
                if value:
                    attr(value)
                else:
                    attr()
                return
            except:
                class_ = engin_class['class']
                self.action_box[engin_class['class_name']] = class_
                attr = getattr(class_(), engin_class['func'])
                if value:
                    attr(value)
                else:
                    attr()
                return
        except:
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
                rait_engin = {'key': str(), 'token': str(), 'rait': 0}

                # Перебираем сравнение токенов с ключами
                for key_input in action_list.keys():
                    if type(key_input) == tuple:
                        for key in key_input:
                            for token in tokens:
                                rait = fuzz.ratio(key, token)
                                # Находим лучший рейтинг
                                if rait > 70 and rait > rait_engin['rait']:
                                    rait_engin['key'], rait_engin['token'], rait_engin['rait'] = key_input, key, rait
                    else:
                        key = key_input
                        for token in tokens:
                            rait = fuzz.ratio(key, token)
                            # Находим лучший рейтинг
                            if rait > 70 and rait > rait_engin['rait']:
                                rait_engin['key'], rait_engin['token'], rait_engin['rait'] = key, key, rait
                # Если нашли нужные ключи
                if rait_engin['rait'] != 0:
                    print(rait_engin)
                    # Вытаскиваем индекс токена подошедшего
                    index = tokens.index(rait_engin['token'])
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
                print(result)
                # Если функция строка отправляем запроснику для обработки
                if type(result['action']) == str:
                    yield {**result, 'text': text}
                else:
                    # Если функция это какая то реальная функция то запускаем её работу
                    self.action_start({**result, 'text': text})
                    yield -1
            else:
                break

        # Нужно или обрабатывать тут функции и запоминать потоки или вернуть обратно для записи их существование
        # Если исполняемые на моменте то нечего

if __name__ == '__main__':
    action_controll = Action_controll()

    while True:
        text = input('TEXT = ')
        for row in action_controll.search_fuction(f'найди {text}', 0):
            print(row)
        print(action_controll.action_box)

if __name__ == 'Assistent_capabilities':
    action_controll = Action_controll()



"""
Список вункций
1. Удалить историю браузера
2.Открытие ссылок
3.Работа с сйтами
3.1. Работа с видео

"""
