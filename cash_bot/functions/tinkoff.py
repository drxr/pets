from PyPDF2 import PdfReader
import pandas as pd


# ОБработчик pdf от Тиньков
def tinkoff_cleaner(src):
    temp_list = []
    itog = []
    reader = PdfReader(src)
    text = ''
    for i in range(len(reader.pages)):
        text += reader.pages[i].extract_text()
    text = text.split('\n')
    income = pd.to_numeric(text[-3].split('RUB')[0].replace(',', '.').split(' ', 2)[-1].replace(' ', ''))
    expend = pd.to_numeric(text[-4].split('RUB')[0].replace(',', '.').split(' ', 2)[-1].replace(' ', ''))
    text = text[16:-4]
    for i in range(len(text)):
        el = text[i].replace('+ ', '+').replace('- ', '-').replace(' ₽', '').split(' ', 7)
        temp_list.append(el)
    for el in temp_list:
        if el[3][0] == '+':
            el = [el[0], el[3][1] + el[4].replace(',', '.'), 0, el[-1]]
        else:
            el = [el[0], 0, el[3][1] + el[4].replace(',', '.'), el[-1]]
    itog.append(el)
    df = pd.DataFrame(itog, columns=['date', 'income', 'expend', 'description'])
    df['bank'] = 'Tinkoff'
    for col in ['income', 'expend']:
        df[col] = pd.to_numeric(df[col])
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    if df.income.sum() == income and df.expend.sum() == expend:
        df_message = 'Файл обработан корректно: сумма доходов и расходов датасета совпадает с оборотами из исходного файла\nДобавлено {df.shape[0]} записей.'
    else:
        df_message = 'Файл обработан с ошибками'
    return df_message


if __name__ == '__main__':
    tinkoff_cleaner(src)
