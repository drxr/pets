from PyPDF2 import PdfReader
import pandas as pd


# Обработчик pdf от ВТБ
def vtb_cleaner(src):
    temp_list = []
    reader = PdfReader(src)
    text = ''
    for i in range(len(reader.pages)):
        text += reader.pages[i].extract_text()
    text = text.split('\n')
    for i in range(len(text)):
        el = (
            text[i].replace('0Перевод', '0 Перевод')
                    .replace('0Оплата', '0 Оплата')
                    .replace('0Перечисление', '0 Перечисление')
                    .replace('0Внутрибанковский', '0 Внутрибанковский')
                    .replace('0(', '0 (')
                    .replace('018201061201010000610;ст.', '0 18201061201010000610;ст.')
                    .split(' ', 6)
            )
        if len(el) >= 3 and el[2] == 'RUB':
            el[0] = text[i - 1]
            temp_list.append(el)
    income = pd.to_numeric(text[4].split(' ')[-2])
    expend = pd.to_numeric(text[5].split(' ')[-2])
    df = pd.DataFrame(temp_list, columns = ['date', 'value', 'currency', 'income', 'expend', 'debt', 'description'])
    df = df.drop(columns=['value', 'currency', 'debt'])
    df['bank'] = 'VTB'
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
    for col in ['income', 'expend']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    if df.income.sum() == income and df.expend.sum() == expend:
        df_message = f'Файл обработан корректно: сумма доходов и расходов датасета совпадает с оборотами из исходного файла\nДобавлено {df.shape[0]} записей.'
    else:
        df_message = 'Файл обработан с ошибками'
    return df_message

if __name__ == '__main__':
    vtb_cleaner(src)
