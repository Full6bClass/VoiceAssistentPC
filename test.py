from fuzzywuzzy import fuzz


def token_search(token, action_list):
    rait_engin = {'key': str(), 'rait': 0}
    for key in action_list.keys():
        rait = fuzz.ratio(key, token)
        if rait > 70 and rait > rait_engin['rait']:
            rait_engin['key'], rait_engin['rait'] = key, rait

    if rait_engin['rait'] != 0:
        result = action_list[rait_engin['key']]
        if isinstance(result, dict):
            return None  # Возвращаем None, если значение - словарь
        else:
            return result
    else:
        return None


def process_command(text):
    # Разбираем текст на токены
    tokens = text.split()
    all_action_list = {
        'стоп': 'stop',
        'звук': {
            'убавить': 'voice_low',
            'прибавить': 'voice_high'
        }
    }

    results = []

    for token in tokens:
        action = token_search(token, action_list=all_action_list)
        if action is not None:
            results.append((token, action))

    return results if results else False  # Если нет результатов, возвращаем False


# Пример использования
command1 = "убавить звук стоп"
matched_actions1 = process_command(command1)
print(matched_actions1)  # Ожидается: [('убавить', 'voice_low'), ('стоп', 'stop')]

command2 = "звук"
matched_actions2 = process_command(command2)
print(matched_actions2)  # Ожидается: False
