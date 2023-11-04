import os
import yadisk
from tqdm import tqdm
from cfg import app_id, secret_id, ya_token
from main import LOAD_PATH
import excel_converter


def load_files():
    # создаем подключение к яндекс диску
    y = yadisk.YaDisk(app_id, secret_id, ya_token)

    # проверяем валидность токена
    if y.check_token():
        print('Token is valid')
    else:
        print('Check OAUTH token')

    # создаем список с именами файлов
    list_of_files = []
    for el in list(y.listdir('for_test')):
        if el['path'].endswith('.xlsx'):
            list_of_files.append(el['path'].split('disk:/')[1])

    # создаем папку загрузки
    if not os.path.exists(LOAD_PATH):
        os.mkdir(LOAD_PATH)
        print('Directory created: ', LOAD_PATH)
    os.chdir(LOAD_PATH)

    # загружаем файлы
    print('Downloading files from yandex disk:')
    for file in tqdm(list_of_files, colour='#FC46AA'):
        y.download(file, file.split('/')[-1])
    print(f'Download complete. {len(os.listdir())} files in work folder.')
    excel_converter.convert_excel()