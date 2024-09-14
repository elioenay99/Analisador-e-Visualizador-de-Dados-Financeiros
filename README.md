# Bot do Telegram para Informações sobre Ações

Este projeto é um bot do Telegram que fornece informações em tempo real sobre ações específicas, utilizando a API da Alpha Vantage. O bot permite que os usuários recebam dados básicos ou detalhados sobre ações, incluindo a opção de baixar esses dados em formato CSV para análise adicional.

## Índice

- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Configuração](#configuração)
- [Execução](#execução)
- [Uso](#uso)
- [Desenvolvimento Futuro](#desenvolvimento-futuro)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## Funcionalidades

- **Consulta de Informações Básicas**: Solicite informações como preço de abertura, alta, baixa, fechamento e volume de uma ação específica.
- **Download de Dados Detalhados**: Baixe um arquivo CSV com dados detalhados, incluindo média móvel de 30 dias e variação percentual diária.
- **Atualizações em Tempo Real**: Receba dados atualizados em tempo real diretamente no Telegram.
- **Interface Intuitiva**: Interaja com o bot através de comandos simples e diretos.

## Pré-requisitos

- **Python 3.8 ou superior**
- Bibliotecas Python:
  - `python-telegram-bot`
  - `pandas`
  - `requests`
- **Chave de API da Alpha Vantage**: Necessária para acessar os dados financeiros.

## Configuração

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/elioenay99/Analisador-e-Visualizador-de-Dados-Financeiros.git
   cd Analisador-e-Visualizador-de-Dados-Financeiros
   ```

2. **Instale as Dependências**

   ```bash
   pip install python-telegram-bot pandas requests
   ```

3. **Obtenha a Chave de API da Alpha Vantage**

   - Registre-se em [Alpha Vantage](https://www.alphavantage.co/support/#api-key) para obter uma chave de API gratuita.
   - Crie um arquivo `config.py` na raiz do projeto e adicione sua chave:

     ```python
     CHAVE = 'SUA_CHAVE_DE_API_AQUI'
     ```

4. **Configure o Token do Bot do Telegram**

   - Obtenha um token para o seu bot através do [BotFather](https://t.me/botfather) no Telegram.
   - No arquivo `main.py`, substitua `SEU_TOKEN_TELEGRAM` pelo token fornecido:

     ```python
     updater = Updater('SEU_TOKEN_TELEGRAM', use_context=True)
     ```

## Execução

Para iniciar o bot, execute o seguinte comando no terminal:

```bash
python main.py
```

O bot estará ativo e pronto para interagir no Telegram.

## Uso

- **Inicie uma Conversa**

  - Procure pelo seu bot no Telegram e inicie uma conversa enviando `/start`.

- **Solicite Informações sobre Ações**

  - Siga as instruções fornecidas pelo bot para consultar informações básicas ou detalhadas sobre ações específicas.

- **Baixe Dados em CSV**

  - Utilize o comando apropriado para receber um arquivo CSV com dados detalhados para análise.

## Desenvolvimento Futuro

Planejamos expandir este projeto com as seguintes funcionalidades:

- **Gráficos de Análise Técnica**: Inclusão de gráficos para melhor visualização dos dados.
- **Suporte a Mais Dados Financeiros**: Adição de indicadores financeiros adicionais.
- **Integração com Outras APIs**: Suporte para outras fontes de dados de mercado.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests no [repositório do projeto](https://github.com/elioenay99/Analisador-e-Visualizador-de-Dados-Financeiros).

