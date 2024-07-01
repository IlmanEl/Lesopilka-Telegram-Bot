# 7283155713:AAEWUbsjB9s21_f_SFzuEXF-sx1wntMd9nE

import logging
from telegram import Update, ForceReply, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import pandas as pd
from datetime import datetime

# Ведение логов
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Инициализация глобальных переменных
expenses = []
approved_users = []
investors = {"Инвестор 1": 1, "Инвестор 2": 2}

# Функция для старта бота
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Введите кодовое слово для начала работы.')

# Функция для проверки кодового слова
def check_code(update: Update, context: CallbackContext) -> None:
    code = update.message.text.lower()
    if code == "лесопилка":
        approved_users.append(update.message.from_user.id)
        update.message.reply_text('Кодовое слово верно. Теперь вы можете вводить расходы.')
    else:
        update.message.reply_text('Неверное кодовое слово. Попробуйте снова.')

# Функция для записи расходов
def add_expense(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in approved_users:
        update.message.reply_text('Введите кодовое слово для доступа.')
        return
    
    try:
        data = update.message.text.split(',')
        item, amount, note, investor = data[0], float(data[1]), data[2] if len(data) > 2 else '', data[3] if len(data) > 3 else ''
        date = datetime.now().strftime('%d.%m.%Y')
        investor_id = investors.get(investor, None)
        expense = {
            'Дата': date,
            'Расход': item,
            'Сумма': amount,
            'Примечание': note,
            'Инвестор': investor_id
        }
        expenses.append(expense)
        update.message.reply_text('Расход добавлен.')
    except Exception as e:
        update.message.reply_text('Ошибка при добавлении расхода. Проверьте формат данных.')

# Функция для просмотра расходов
def view_expenses(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in approved_users:
        update.message.reply_text('Введите кодовое слово для доступа.')
        return

    df = pd.DataFrame(expenses)
    if df.empty:
        update.message.reply_text('Пока нет записей о расходах.')
    else:
        update.message.reply_text(df.to_string())

# Функция для удаления расходов
def delete_expense(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in approved_users:
        update.message.reply_text('Введите кодовое слово для доступа.')
        return

    try:
        expense_id = int(update.message.text.split(' ')[1])
        del expenses[expense_id]
        update.message.reply_text('Запись удалена.')
    except Exception as e:
        update.message.reply_text('Ошибка при удалении записи.')

# Функция для сохранения расходов в Excel
def save_to_excel(filename='expenses.xlsx'):
    df = pd.DataFrame(expenses)
    df.to_excel(filename, index=False)

def save_expenses(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in approved_users:
        update.message.reply_text('Введите кодовое слово для доступа.')
        return

    try:
        save_to_excel()
        update.message.reply_text('Данные сохранены.')
    except Exception as e:
        update.message.reply_text('Ошибка при сохранении данных.')

# Функция для скачивания Excel файла
def download_excel(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in approved_users:
        update.message.reply_text('Введите кодовое слово для доступа.')
        return

    try:
        save_to_excel()
        update.message.reply_document(document=InputFile('expenses.xlsx'))
    except Exception as e:
        update.message.reply_text('Ошибка при скачивании файла.')

def main():
    # Вставь сюда свой токен API
    updater = Updater("7283155713:AAEWUbsjB9s21_f_SFzuEXF-sx1wntMd9nE", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("view", view_expenses))
    dp.add_handler(CommandHandler("delete", delete_expense))
    dp.add_handler(CommandHandler("save", save_expenses))
    dp.add_handler(CommandHandler("download", download_excel))
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_code))
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_expense))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
