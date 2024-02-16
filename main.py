from telegram.ext import Updater, CommandHandler, CallbackContext
from functions import fetch_stock_data, analyze_data, export_data, format_data_message
from config import CHAVE_TELEGRAM as TOKEN


def fetch_data(update, context):
    symbol = 'AAPL'  # Exemplo de símbolo de ação
    df = fetch_stock_data(symbol)
    analyzed_df = analyze_data(df)

    # Utiliza a função format_data_message para formatar os dados
    message = format_data_message(analyzed_df, symbol)

    update.message.reply_text(message)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("fetch_data", fetch_data))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
