from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import make_row_keyboard
from functions import sql_connector
from reports import vizualization
from handlers.states import ChangeFinances, available_operations


router = Router()

# Обработчик команды старт
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer('''Привет! Вот, что я умею:
    1. Читать pdf выписки из Тиньков и ВТБ - просто загрузи их в чат
    2. Читать эксель таблицу в формате от Кати Сапожниковой - просто загрузи в чат
    3. Читать операции из чата в формате: приход/расход, дд.мм.гггг, сумма, банк, описание
    4. Сделать общую выгрузку по доходам и расходам из базы данных по команде /get_data
    5. Добавлять операции через команду /operation''')

# Обработчик команды отмена
@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
# Точка входа в FSM (последовательные шаги для добавления операции) команда operation
@router.message(Command("operation"))
async def cmd_operation(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите тип операции:",
        # клавиатура для ответа из файла keyboards, переменная для клавиатуры из файла states
        # см. импорты
        reply_markup=make_row_keyboard(available_operations)
    )
    # Устанавливаем пользователю состояние "выбирает операцию"
    await state.set_state(ChangeFinances.choosing_operation)

# Обработчик команды get_data
# Возвращает всю базу данных в виде csv файла (дополнительно отправляет график)
@router.message(Command("get_data"))
async def get_data(message: Message):
    sql_connector.get_budget(message.from_user.username)
    vizualization.draw_pie()
    # Для чтения и отправки файла из файловой системы используем FSInputFile
    message_from_pc = FSInputFile("/projects/final_bot/files/all_data.csv")
    await message.answer_document(message_from_pc)
    image_from_pc = FSInputFile("/projects/final_bot/files/fig1.png")
    await message.answer_photo(image_from_pc)
