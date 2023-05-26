import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import sql_connector

def draw_pie():
    'Функция для отрисовки пирога с долями доходов и расходов'
    df = pd.read_csv('/projects/final_bot/files/all_data.csv', index_col=0)
    colors = sns.color_palette('pastel')[0:5]
    data = [sum(df.income.to_list()), sum(df.expend.tolist())]
    labels=['income', 'outcome']
    plt.pie(data, labels = labels, colors = colors, autopct='%.0f%%')
    plt.savefig('/projects/final_bot/files/fig1.png')
