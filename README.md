
# Bot do Telegram para Informações sobre Ações

Este projeto é um bot do Telegram que fornece informações em tempo real sobre ações específicas. Utiliza a API da Alpha Vantage para buscar dados financeiros e permite aos usuários receber informações compactas ou detalhadas sobre ações, incluindo a opção de baixar esses dados em formato CSV.

## Funcionalidades

- **Consulta de informações básicas**: Os usuários podem solicitar informações básicas sobre uma ação, incluindo preço de abertura, alta, baixa, fechamento e volume.
- **Download de dados detalhados**: Os usuários têm a opção de baixar um conjunto de dados mais detalhado em formato CSV, incluindo a média móvel de 30 dias e a variação percentual diária.

## Pré-requisitos

- Python 3.8 ou superior
- Biblioteca `python-telegram-bot`
- Biblioteca `pandas`
- Acesso à API da Alpha Vantage (requer uma chave de API)

## Configuração

1. Clone o repositório para a sua máquina local.
2. Instale as dependências necessárias utilizando o pip:

    ```bash
    pip install python-telegram-bot pandas requests
    ```

3. Obtenha uma chave de API gratuita da [Alpha Vantage](https://www.alphavantage.co/support/#api-key) e adicione-a ao arquivo `config.py`:

    ```python
    CHAVE = 'SUA_CHAVE_DE_API_AQUI'
    ```

4. Substitua `SEU_TOKEN_TELEGRAM` no arquivo `main.py` pelo token do seu bot, obtido através do [BotFather](https://t.me/botfather) no Telegram.

## Execução

Para iniciar o bot, execute o arquivo `main.py`:

```bash
python main.py
```

O bot agora estará rodando e pronto para interagir com os usuários através do Telegram.

## Uso

- Envie `/start` para o bot para iniciar a interação e ver as opções disponíveis.
- Siga as instruções do bot para solicitar informações sobre ações ou baixar dados.

## Desenvolvimento Futuro

Este projeto pode ser expandido com funcionalidades adicionais, como a inclusão de gráficos para análise técnica, suporte para mais tipos de dados financeiros e integração com outras APIs de dados de mercado.