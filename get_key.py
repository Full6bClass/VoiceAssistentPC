import requests
import uuid

def get_key(key):
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
        'Authorization': f'Basic {key}',
        'RqUID': rq_uid
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=cert_path)
    print(response)
    print(response.text)
    print(response.json())
    return response.text['access_token']

key = 'YmI3ODI3YTYtZDIxYS00MTI3LTlmMmEtMGI2MjI0NDM5MThiOjM1ODA0YWY2LTA1OGUtNDkxMC1iMjMzLTRkNmRiOGYzNTg1OA=='
get_key(key)


