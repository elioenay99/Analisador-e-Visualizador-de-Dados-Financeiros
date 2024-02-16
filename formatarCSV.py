import pandas as pd


def traduzir_e_formatar_csv(arquivo_entrada, arquivo_saida):
    # Leitura do CSV
    df = pd.read_csv(arquivo_entrada)

    # Tradução das Colunas
    colunas_traduzidas = {
        'open': 'Abertura',
        'high': 'Máxima',
        'low': 'Mínima',
        'close': 'Fechamento',
        'volume': 'Volume',
        '30_day_moving_avg': 'Média de movimentação em 30 dias',
        'daily_pct_change': 'Movimentação diária'
    }
    df.rename(columns=colunas_traduzidas, inplace=True)

    # Formatação de volume para o padrão brasileiro
    df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.2f}".replace(',', 'temp').replace('.', ',').replace('temp', '.'))

    # Exportação do CSV traduzido e formatado
    df.to_csv(arquivo_saida, index=False)

