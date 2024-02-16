import pandas as pd
import requests
from config import CHAVE as api_key


def fetch_stock_data(symbol):
    """Busca dados históricos de ações da API e retorna como DataFrame."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "compact"
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Converte os dados em DataFrame
    df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index', dtype=float)
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index = pd.to_datetime(df.index)

    return df


def analyze_data(df):
    """Adiciona análises ao DataFrame, como média móvel e variação percentual diária."""
    df['30_day_moving_avg'] = df['close'].rolling(window=30).mean()
    df['daily_pct_change'] = df['close'].pct_change() * 100

    return df


def export_data(df, filename):
    """Exporta DataFrame para arquivo CSV."""
    df.to_csv(filename)
    print(f"Dados exportados para {filename}.")


def format_data_message(df, symbol):
    """Formata uma mensagem com os últimos dados disponíveis do DataFrame para envio pelo Telegram."""
    if not df.empty:
        last_row = df.iloc[-1]
        message = (f"Dados mais recentes para {symbol}:\n"
                   f"Data: {last_row.name.strftime('%Y-%m-%d')}\n"
                   f"Abertura: {last_row['open']:.2f}\n"
                   f"Alta: {last_row['high']:.2f}\n"
                   f"Baixa: {last_row['low']:.2f}\n"
                   f"Fechamento: {last_row['close']:.2f}\n"
                   f"Volume: {last_row['volume']:,}\n"
                   f"Variação Percentual Diária: {last_row['daily_pct_change']:.2f}%")
    else:
        message = "Não foi possível obter os dados."

    return message
