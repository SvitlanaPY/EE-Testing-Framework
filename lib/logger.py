import datetime
import os
from requests import Response

# в класі буде два методи: add_request (логування запиту) та add_response(логування відповіді), і один метод, який буде записувати отриманий текст логу в лог-файл
# сам файл ми виносимо як змінну класу, назва файлу буде містити дату та час запуску тестів з точністю до секунди, щоб не перезаписувати попередні логи
# таким чином для різних запусків тестів будуть створюватися різні лог-файли, і ми зможемо відстежувати історію запитів та відповідей
# Оскільки наш Logger буде працювати з часом, то ми імпортуємо модуль datetime, щоб отримувати поточний час та дату для назви файлу та для запису часу запиту та відповіді в лог-файл

class Logger:
    file_name = f"logs/log_" + str(datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")) + ".log"

    # метод для запису логу в файл, який буде відкривати файл у режимі додавання (append) та записувати отриманий текст логу в кінець файлу
    # ми написали зазву методу з підкресленням _write_log_to_file, щоб показати, що цей метод є приватним і не повинен викликатися ззовні класу Logger, а використовуватись лише всередині класу Logger
    @classmethod
    def _write_log_to_file(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    # метод, який буде отримувати дані запиту, формувати їх у якусь строку і віддавати її у метод _write_lo_t_file
    # метод add_request буде отримувати такі параметри: url (адреса запиту), data (дані запиту), headers (заголовки запиту), cookies (кукі запиту), json (json-дані запиту) та method (метод запиту: GET, POST, PUT, DELETE)
    # усе це ми будемо перетворювати у строку та передавати у метод _write_log_to_file, щоб записати у лог-файл
    # os.environ.get('PYTEST_CURRENT_TEST') - говорить про те, який саме тест виконується зараз, і як він називається, щоб ми могли відстежувати, який саме тест викликав цей запит
    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, json: dict, method: str):
        test_name = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Time: {datetime.datetime.now()}\n"
        data_to_add += f"Request Method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request Data: {data}\n"
        data_to_add += f"Request Headers: {headers}\n"
        data_to_add += f"Request Cookies: {cookies}\n"
        data_to_add += f"Request JSON: {json}\n"
        data_to_add += "\n"

        cls._write_log_to_file(data_to_add)

    # метод, який буде отримувати дані відповіді, формувати їх у якусь строку і віддавати її у метод _write_log_to_file
    # метод add_response буде отримувати параметр response (об'єкт відповіді від сервера), з якого ми будемо отримувати статус-код відповіді, текст відповіді, заголовки відповіді та кукі відповіді, і формувати їх у строку, яку ми будемо передавати у метод _write_log_to_file, щоб записати у лог-файл
    # ми будемо перетворювати cookies та headers у словники, щоб вони були більш зручними для читання у лог-файлі
    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response Status Code: {response.status_code}\n"
        data_to_add += f"Response Text: {response.text}\n"
        data_to_add += f"Response Headers: {headers_as_dict}\n"
        data_to_add += f"Response Cookies: {cookies_as_dict}\n"

        cls._write_log_to_file(data_to_add)
