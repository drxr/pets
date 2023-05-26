import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd


# Подключаемся к базе данных
engine = create_engine('sqlite:///C://projects/final_bot/finances.db', echo=False)

# Функция проверяем наличие таблицы пользователи и если нет - создает ее
def create_table(name):
    sql_query = \
    f'''
    CREATE TABLE IF NOT EXISTS {name} (
    "index" INTEGER NOT NULL,
    date DATE,
    income FLOAT,
    expend FLOAT,
    description VARCHAR(100),
    bank VARCHAR(20)
    );
    '''
    engine.execute(sql_query)

# Функция считает количество записей в базе данных
def find_count(name):
    sql_query = \
    f'''
    SELECT COUNT(*) FROM {name};
    '''
    return engine.execute(sql_query).fetchone()[0]

# Функция выгрузки всех записей из базы данных и перевод в csv
def get_budget(name):
    sql_query = \
    f'''
    SELECT *
    FROM {name};
    '''
    df = pd.read_sql(sql_query, con=engine)
    df = df.drop(columns='index')
    df.to_csv('/projects/final_bot/files/all_data.csv')

# Функция добавления записей в базу данных
def add_operation(name, is_now, income, expend, bank):
    sql_query = \
    f'''
    INSERT INTO {name} ("index", date, income, expend, description, bank)
    VALUES ({find_count(f'{name}')}, {is_now}, {income}, {expend}, 'test', 'f"{bank}"')
    '''
    engine.execute(sql_query)
