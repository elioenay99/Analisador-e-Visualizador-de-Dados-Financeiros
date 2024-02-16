from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, \
    MessageHandler, Filters
from functions import fetch_stock_data, analyze_data, export_data, format_data_message
from config import CHAVE_TELEGRAM as TOKEN

SYMBOL = 0


def start(update: Update, context: CallbackContext) -> int:
    keyboard = [[InlineKeyboardButton("Clique aqui para informar o símbolo da ação", callback_data='get_symbol')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Por favor, escolha uma opção:', reply_markup=reply_markup)
    return SYMBOL


def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Por favor, digite o símbolo da ação:")
    return SYMBOL


def get_symbol(update: Update, context: CallbackContext) -> int:
    symbol = update.message.text.upper()
    df = fetch_stock_data(symbol)
    if df.empty:
        update.message.reply_text("Não foi possível encontrar dados para a ação especificada.")
        return ConversationHandler.END
    analyzed_df = analyze_data(df)
    message = format_data_message(analyzed_df, symbol)
    send_info_with_download_option(update, context, message, symbol)
    return ConversationHandler.END


def send_info_with_download_option(update, context, message, symbol):
    keyboard = [[InlineKeyboardButton("Baixar CSV com Mais Informações", callback_data=f'download_{symbol}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)


def download_data(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    symbol = query.data.split('_')[1]
    df_full = fetch_stock_data(symbol, outputsize="full")
    analyzed_df_full = analyze_data(df_full)
    file_path = f"{symbol}_full_data.csv"
    export_data(analyzed_df_full, file_path)
    with open(file_path, 'rb') as file:
        context.bot.send_document(chat_id=query.message.chat_id, document=file, filename=file_path)
    query.message.delete()


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operação cancelada.')
    return ConversationHandler.END


def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SYMBOL: [CallbackQueryHandler(button, pattern='^get_symbol$'),
                     MessageHandler(Filters.text & ~Filters.command, get_symbol)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(download_data, pattern='^download_'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
