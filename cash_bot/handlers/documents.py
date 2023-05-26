from aiogram import Router, F, Bot
from aiogram.types import Message
from functions import common, vtb, tinkoff, sql_connector
import pandas as pd

router = Router()

# Обработчик документов, которые кидают в чат боту
@router.message(F.document)
async def download_photo(message: Message, bot: Bot):
    file_info = await bot.get_file(message.document.file_id)
    src = 'C://projects/final_bot/files/' + message.document.file_name
    await bot.download_file(file_info.file_path, src)
    test = await bot.download_file(file_info.file_path)
    doc_type = message.document.file_name.split('.')[-1]
    with open(src) as file:
        if doc_type == 'pdf':
            bank = common.bank_finder(src)
        elif doc_type in ['xls', 'xlsx']:
            bank = None
    with open(src) as new_file:
        if bank == 'втб':
            vtb.vtb_cleaner(src)
            await message.answer(vtb.vtb_cleaner(src))
        elif bank == 'тинькофф':
            tinkoff.tinkoff_cleaner(src)
            await message.answer(tinkoff.tinkoff_cleaner(src))
        else:
            common.xls_converter(src)
            await message.answer(common.xls_converter(src))
    db_user = message.from_user.username
    sql_connector.create_table(db_user)
    df = pd.read_csv('c://projects/final_bot/files/bank_data.csv', index_col=0)
    df.to_sql(db_user, con=sql_connector.engine, if_exists='append')
    await message.answer('конец работы обработчика')
