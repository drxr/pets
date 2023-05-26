from PyPDF2 import PdfReader
import pandas as pd
import openpyxl


# функция определения банка в pdf файле
def bank_finder(src):
    file = open(src, 'rb')
    reader = PdfReader(file)
    text = ''
    for i in range(len(reader.pages)):
        text += reader.pages[i].extract_text()
    work = text
    work = work.split('\n')
    if 'втб' in work[-2].lower():
        return 'втб'
    elif 'тинькофф' in work[7].lower():
        return 'тинькофф'
    return 'others'
    file.close()

# Функция для обработки эксель файлов в формате от Кати Сапожниковой
# Можно сделать в 4 строки через pandas.read_excel(), но лень переписывать назад
def xls_converter(src):
    f = openpyxl.load_workbook(src)
    ws = f.active
    data = ws.values
    cols = next(data)
    data = list(data)
    df = pd.DataFrame(data, columns=cols)
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа']).dt.date
    df = df.reset_index(drop=True)
    df.columns = ['date', 'description', 'summ', 'cat', 'subcat', 'bank', 'type']
    #df.date = pd.to_datetime(df.date).dt.date
    df['income'] = df.apply(lambda cell: cell.summ if cell.type == 'доход' else 0, axis=1)
    df['expend'] = df.apply(lambda cell: cell.summ if cell.type == 'расход' else 0, axis=1)
    df = df[['date', 'income', 'expend', 'description', 'bank']]
    df.to_csv('/projects/final_bot/files/bank_data.csv')
    df_message = f'Добавлено {df.shape[0]} записей.'
    return df_message
