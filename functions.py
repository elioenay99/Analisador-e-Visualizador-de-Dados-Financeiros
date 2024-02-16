import pandas as pd
import requests
from config import CHAVE as api_key


def fetch_stock_data(symbol, outputsize="compact"):
    """
    Busca dados históricos de ações da API Alpha Vantage e retorna como DataFrame.

    Args:
        symbol (str): Símbolo da ação.
        outputsize (str, optional): Tamanho da saída. Padrão: "compact".

    Returns:
        DataFrame: DataFrame com dados históricos da ação.
    """
    try:
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
    except Exception as e:
        print(f"Erro ao buscar dados para {symbol}: {e}")
        return pd.DataFrame()


def analyze_data(df):
    """
    Adiciona análises ao DataFrame, como média móvel e variação percentual diária.

    Args:
        df (DataFrame): DataFrame com dados históricos da ação.

    Returns:
        DataFrame: DataFrame com as análises adicionais.
    """
    if not df.empty:
        df['30_day_moving_avg'] = df['close'].rolling(window=30, min_periods=1).mean()
        df['daily_pct_change'] = df['close'].pct_change() * 100
    return df


def export_data(df, filename):
    """
    Exporta DataFrame para arquivo CSV.

    Args:
        df (DataFrame): DataFrame a ser exportado.
        filename (str): Nome do arquivo CSV.
    """
    df.to_csv(filename)
    print(f"Dados exportados para {filename}.")


def format_data_message(df, symbol):
    """
    Formata uma mensagem com as informações mais recentes de uma ação.

    Args:
        df (DataFrame): DataFrame com dados históricos da ação.
        symbol (str): Símbolo da ação.

    Returns:
        str: Mensagem formatada com as informações da ação.
    """
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


def format_symbol(symbol, is_brazilian):
    """
    Formata o símbolo da ação de acordo com o tipo (brasileira ou internacional).

    Args:
        symbol (str): Símbolo da ação.
        is_brazilian (bool): Indica se a ação é brasileira.

    Returns:
        str: Símbolo da ação formatado.
    """
    if is_brazilian and not symbol.endswith(".SA"):
        symbol += ".SA"
    return symbol
