import pandas as pd
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def traduzir_e_formatar_csv(arquivo_entrada, arquivo_saida):
    logger.info(f"Iniciando a tradução e formatação do arquivo: {arquivo_entrada}")

    try:
        # Leitura do CSV
        df = pd.read_csv(arquivo_entrada)
        logger.info("Arquivo CSV lido com sucesso.")
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
        logger.info("Colunas traduzidas.")
        # Formatação de volume para o padrão brasileiro
        df['Volume'] = df['Volume'].apply(
            lambda x: f"{x:,.2f}".replace(',', 'temp').replace('.', ',').replace('temp', '.'))
        logger.info("Dados formatados.")
        # Exportação do CSV traduzido e formatado
        df.to_csv(arquivo_saida, index=False)
        logger.info(f"Arquivo CSV traduzido e formatado exportado com sucesso: {arquivo_saida}")

    except Exception as e:
        logger.error(f"Erro ao traduzir e formatar o arquivo: {e}")
