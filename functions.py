import pandas as pd
import requests
from config import CHAVE as api_key


def fetch_stock_data(symbol, outputsize="compact"):
    """Busca dados históricos de ações da API e retorna como DataFrame."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": outputsize
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'Time Series (Daily)' in data:
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index').astype(float)
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df.index = pd.to_datetime(df.index)
        return df
    else:
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de falha na obtenção dos dados.


def analyze_data(df):
    """Adiciona análises ao DataFrame, como média móvel e variação percentual diária."""
    if not df.empty:
        df['30_day_moving_avg'] = df['close'].rolling(window=30, min_periods=1).mean()
        df['daily_pct_change'] = df['close'].pct_change() * 100
    return df


def export_data(df, filename):
    """Exporta DataFrame para arquivo CSV."""
    df.to_csv(filename)
    print(f"Dados exportados para {filename}.")


def format_data_message(df, symbol):
    """Formata uma mensagem com as informações mais recentes de uma ação."""
    if not df.empty:
        last_row = df.iloc[-1]
        message = (f"Dados mais recentes para {symbol}:\n"
                   f"Data: {last_row.name.strftime('%Y-%m-%d')}\n"
                   f"Abertura: {last_row['open']:.2f}\n"
                   f"Alta: {last_row['high']:.2f}\n"
                   f"Baixa: {last_row['low']:.2f}\n"
                   f"Fechamento: {last_row['close']:.2f}\n"
                   f"Volume: {last_row['volume']:,.0f}\n"
                   f"Média Móvel de 30 dias: {last_row.get('30_day_moving_avg', 'N/A')}\n"
                   f"Variação Percentual Diária: {last_row.get('daily_pct_change', 'N/A')}")
    else:
        message = "Não foi possível obter os dados para essa ação."
    return message
