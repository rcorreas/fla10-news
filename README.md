# Fla10 News - Redação Automatizada

Sistema de geração automática de notícias do Flamengo usando inteligência artificial.

## Funcionalidades

- **Busca Automática**: Coleta notícias via RSS de fontes esportivas
- **Filtro Inteligente**: Identifica automaticamente notícias sobre o Flamengo
- **Geração com IA**: Cria artigos completos usando modelos de linguagem
- **Interface Web**: Painel de controle intuitivo com Streamlit
- **Armazenamento Local**: Salva artigos em formato Markdown

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/fla10-news.git
cd fla10-news
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
streamlit run app.py
```

## Uso

1. Acesse `http://localhost:8501` no navegador
2. Clique em "Buscar Novas Notícias" na sidebar
3. Visualize as notícias encontradas
4. Clique em "Gerar Artigos" para criar conteúdo com IA
5. Salve os artigos gerados localmente

## Estrutura do Projeto

- `app.py`: Interface principal Streamlit
- `news_fetcher.py`: Módulo de busca RSS
- `article_generator.py`: Geração de artigos com IA
- `config.py`: Configurações do sistema
- `articles/`: Diretório para artigos salvos

## Configuração

Edite `config.py` para:
- Adicionar novos feeds RSS
- Alterar modelo de IA
- Configurar limites de busca

## Tecnologias

- Python 3.9+
- Streamlit
- Feedparser
- Hugging Face Inference API

## Licença

MIT