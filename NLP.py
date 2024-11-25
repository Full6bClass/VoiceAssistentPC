import re
import re
from num2words import num2words
from words2numsrus.extractor import NumberExtractor


class Text_spliter:
    def __init__(self, text):
        self.text = text
        self.proposal_list = []
        # Регулярное выражение для разбиения текста на предложения
        self.proposal_split_pattern = r'([.!?:\n])'

    def split_to_proposal(self):
        # Используем re.split для разбивки текста
        sentences = re.split(self.proposal_split_pattern, self.text)

        # Объединяем предложения и знаки препинания
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i].strip() + sentences[i + 1].strip()
            if sentence:
                self.proposal_list.append(sentence)

        # Если нет предложений, добавляем весь текст как одно предложение
        if not self.proposal_list:
            self.proposal_list.append(self.text)

    def proposal_list_optimized(self, minimal_token=5):
        self.split_to_proposal()
        result = []
        stream_test = False
        for proposal in self.proposal_list:
           token_start = len(proposal.split())
           if stream_test:
               result[-1] += ' ' + proposal
               token_new = result[-1].split()
               if len(token_new) <= minimal_token:
                   stream_test = True
               else:
                   stream_test = False
           else:
               if token_start <= minimal_token:
                  stream_test = True
               else:
                   stream_test = False
               result.append(proposal)
        return result

class Text_stable:

    def numbers_to_words(self, text):
        # Функция для замены чисел на слова
        def replace_match(match):
            number = int(match.group(0))  # Получаем число из совпадения
            return num2words(number, lang='ru')  # Преобразуем число в слово на русском

        # Используем регулярное выражение для поиска чисел в тексте
        return re.sub(r'\b\d+\b', replace_match, text)


    def words_to_numbers(self, text):
        extractor = NumberExtractor()
        return extractor.replace_groups(text)






text = ('Для того чтобы сделать сухарики со вкусом сыра, используют технологию ароматизации продукта. Сырный вкус достигается за счет добавления специальных пищевых добавок – ароматизаторов, которые имитируют вкус сыра. Вот несколько основных этапов этого процесса:'
'7991154. Выбор основы\n'
   'В качестве основы для сухарей чаще всего используется хлеб или батон. Хлеб нарезают на небольшие кусочки, которые затем обжаривают или сушат до хрустящего состояния.'
'68181261671. Приготовление сухарей\n'
   'Нарезанные кусочки хлеба высушиваются при низкой температуре (около 100–120°C), пока они не станут полностью сухими и хрустящими. Этот процесс может занимать от нескольких минут до часа в зависимости от толщины кусочков.'
'102. Добавление масла\n'
   'После сушки сухари могут быть слегка смазаны растительным маслом. Это помогает ароматизатору лучше распределиться по поверхности сухаря.'
'7962. Использование ароматизатора\n'
   'Ароматизаторы могут быть натуральными или искусственными. Натуральные ароматизаторы изготавливаются из экстрактов настоящего сыра, тогда как искусственные – из химических соединений, которые точно воспроизводят сырный вкус.'
   'На этом этапе сухари смешиваются с порошковым ароматизатором, который равномерно распределяется по их поверхности. Важно соблюдать правильную дозировку, чтобы вкус был насыщенным, но не слишком резким.'
'118176161. Охлаждение и упаковк\n'
  'Сухари охлаждают до комнатной температуры и упаковывают в герметичные пакеты, чтобы сохранить свежесть и предотвратить потерю аромата.'
'Таким образом, главное отличие заключается в использовании специального ароматизатора, который придает продукту нужный вкус без необходимости добавлять сам сыр.')

if __name__ == '__main__':
    # text_spliter = Text_spliter(text=text)
    text_stable = Text_stable()

if __name__ == 'NLP':
    text_stable = Text_stable()



