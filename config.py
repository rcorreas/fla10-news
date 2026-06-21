import os
from dotenv import load_dotenv

load_dotenv()

# RSS Feeds do Flamengo
RSS_FEEDS = [
    "https://ge.globo.com/rss/ge/futebol/times/flamengo/",
    "https://esporte.uol.com.br/futebol/campeonatos/brasileirao/rss.xml",
    "https://www.uol.com.br/esporte/futebol/campeonatos/brasileirao/noticias/rss.xml"
]

# Configurações de IA - NVIDIA NIM
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
DEFAULT_MODEL = "meta/llama-3.1-8b-instruct"

# Configurações gerais
ARTICLES_DIR = "articles"
MAX_ARTICLES_PER_FEED = 5
