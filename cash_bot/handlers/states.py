from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters.text import Text
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime

from keyboards.main_keyboard import make_row_keyboard
from functions import sql_connector


router = Router()

# Переменные для клавиатуры
available_operations = ["Приход", "Расход", "Отмена"]
available_banks = ["ВТБ", "Сбер", "Тинькофф", "Другой банк", "Отмена"]

# Класс FSM для пошагового внесения операций
class ChangeFinances(StatesGroup):
    choosing_operation = State()
    choosing_bank = State()
    input_amount = State()

# Операция отмены на текст
@router.message(Text(text="Отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove())

# Этап выбора операции - корректно
@router.message(ChangeFinances.choosing_operation, F.text.in_(available_operations))
async def operation_chosen(message: Message, state: FSMContext):
    await state.update_data(operation_chosen=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите банк:",
        reply_markup=make_row_keyboard(available_banks)
    )
    await state.set_state(ChangeFinances.choosing_bank)

# Этап выбора операции - некорректно
@router.message(ChangeFinances.choosing_operation)
async def operation_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такой тип операции.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_operations)
    )

# Этап выбора банка - корректно
@router.message(ChangeFinances.choosing_bank, F.text.in_(available_banks))
async def bank_chosen(message: Message, state: FSMContext):
    user_data = await state.update_data(bank_chosen=message.text.lower())
    await message.answer(
        text=f"Теперь введите сумму операции в формате рубли.копейки",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ChangeFinances.input_amount)

# Этап выбора банка - некорректно
@router.message(ChangeFinances.choosing_bank)
async def bank_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого банка.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_banks)
    )

# Этап ввода суммы операции
@router.message(ChangeFinances.input_amount)
async def amount_chosen(message: Message, state: FSMContext):
    db_user = message.from_user.username
    sql_connector.create_table(db_user)
    # Собираем данные из FSM
    user_data = await state.get_data()
    # Вносим данные в базу данных
    if user_data['operation_chosen'] == 'приход':
        sql_connector.add_operation(db_user, datetime.now().strftime("%m-%d-%Y"), float(message.text.lower()), 0, str(user_data['bank_chosen']))
    else:
        sql_connector.add_operation(db_user, datetime.now().strftime("%m-%d-%Y"), 0, float(message.text.lower()), str(user_data['bank_chosen']))
    await message.answer(
    text = f"Операция добавлена.\nСумма: {message.text.lower()} \nТип операции: {user_data['operation_chosen']} \nБанк: {user_data['bank_chosen']} {datetime.now().date()}")
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()
