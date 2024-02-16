from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, \
    MessageHandler, Filters
from formatarCSV import traduzir_e_formatar_csv
from functions import fetch_stock_data, analyze_data, export_data, format_data_message, format_symbol
from config import CHAVE_TELEGRAM as TOKEN
import logging
import re

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SYMBOL = 0


def start(update: Update, context: CallbackContext) -> int:
    keyboard = [[
        InlineKeyboardButton("Ações Brasileiras", callback_data='brazil'),
        InlineKeyboardButton("Ações Internacionais", callback_data='international'),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Por favor, escolha o tipo de ação que deseja pesquisar:', reply_markup=reply_markup)

    context.user_data["is_brazilian"] = True
    return SYMBOL


def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    if query.data == 'brazil':
        context.user_data["is_brazilian"] = True
        query.edit_message_text(text="Por favor, digite o símbolo da ação:")
    elif query.data == 'international':
        context.user_data["is_brazilian"] = False
        query.edit_message_text(text="Por favor, digite o símbolo da ação (sem '.SA'):")

    return SYMBOL


def is_valid_symbol(symbol):
    """Valida se o símbolo da ação é alfanumérico e tem um comprimento razoável."""
    return re.match(r'^[0-9A-Za-z.]{1,10}$', symbol)


def get_symbol(update: Update, context: CallbackContext) -> int:
    symbol = update.message.text.upper()
    if not is_valid_symbol(symbol):
        update.message.reply_text("Símbolo da ação inválido. Por favor, verifique e tente novamente.")
        return ConversationHandler.END

    is_brazilian = context.user_data["is_brazilian"]
    symbol = format_symbol(symbol, is_brazilian)

    try:
        df = fetch_stock_data(symbol)
    except Exception as e:
        logger.error(f"Erro ao buscar dados para {symbol}: {e}")
        update.message.reply_text("Houve um erro ao buscar os dados. Por favor, verifique o símbolo e tente novamente.")
        return ConversationHandler.END

    if df.empty:
        update.message.reply_text("Não foi possível encontrar dados para a ação especificada.")
        return ConversationHandler.END

    analyzed_df = analyze_data(df)
    message = format_data_message(analyzed_df, symbol)
    send_info_with_download_option(update, context, message, symbol)
    return ConversationHandler.END


def send_info_with_download_option(update: Update, context: CallbackContext, message, symbol):
    keyboard = [[InlineKeyboardButton("Baixar CSV com Mais Informações", callback_data=f'download_{symbol}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)


def download_data(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    symbol = query.data.split('_')[1]

    try:
        df_full = fetch_stock_data(symbol, outputsize="full")
    except Exception as e:
        logger.error(f"Erro ao buscar dados para {symbol}: {e}")
        query.message.reply_text("Não foi possível encontrar dados para a ação especificada.")
        return

    analyzed_df_full = analyze_data(df_full)
    file_path = f"{symbol}_full_data.csv"
    export_data(analyzed_df_full, file_path)
    arquivo_saida = file_path
    traduzir_e_formatar_csv(file_path, arquivo_saida)
    with open(file_path, 'rb') as file:
        context.bot.send_document(chat_id=query.message.chat_id, document=file, filename=file_path)
    query.message.delete()


def ajuda(update: Update, context: CallbackContext) -> int:
    message = (
        "**Bem-vindo ao Bot de Pesquisa de Ações!**\n\n"
        "Este bot permite que você pesquise informações sobre ações brasileiras e internacionais.\n\n"
        "**Como usar:**\n\n"
        "1. Escolha o tipo de ação que deseja pesquisar:\n"
        "    * Clique no botão 'Pesquisa de Ações Brasileiras'\n"
        "    * Clique no botão 'Pesquisa de Ações Internacionais'\n\n"
        "2. Digite o símbolo da ação que deseja pesquisar.\n\n"
        "3. O bot retornará informações sobre a ação, como preço, volume, média móvel e variação percentual.\n\n"
        "**Dicas:**\n\n"
        "* Para ações brasileiras, digite o símbolo com ou sem '.SA'.\n"
        "* Para ações internacionais, digite o símbolo sem '.SA'.\n\n"
        "**Exemplo:**\n\n"
        "Para pesquisar a ação da Petrobras (PETR4):\n"
        "    * Clique no botão 'Pesquisa de Ações Brasileiras'\n"
        "    * Digite 'PETR4' ou 'petr4'\n\n"
        "**Obrigado por usar o Bot de Pesquisa de Ações!**"
    )
    update.message.reply_text(message)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operação cancelada.')
    return ConversationHandler.END


def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SYMBOL: [CallbackQueryHandler(button, pattern='^(brazil|international)$'),
                     MessageHandler(Filters.text & ~Filters.command, get_symbol)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('help', ajuda)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(download_data, pattern='^download_'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
