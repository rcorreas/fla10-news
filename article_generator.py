import requests
import os
from config import NVIDIA_API_KEY, NVIDIA_API_URL, DEFAULT_MODEL

DIRETRIZES_PATH = os.path.join(os.path.dirname(__file__), "diretrizes_editoriais.md")
EXEMPLOS_PATH = os.path.join(os.path.dirname(__file__), "exemplos_estilo.md")

def load_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def generate_article_from_news(news_item, model=DEFAULT_MODEL, fontes=None):
    diretrizes = load_file(DIRETRIZES_PATH)
    exemplos = load_file(EXEMPLOS_PATH)

    fontes_section = ""
    if fontes:
        fontes_list = "\n".join([f"- {f}" for f in fontes])
        fontes_section = f"""
## FONTES ADICIONAIS FORNECIDAS PELO USUÁRIO:
Use estas fontes para enriquecer a matéria com informações adicionais:
{fontes_list}

Consulte essas fontes para obter detalhes extras, dados, estatísticas, declarações e contexto adicional sobre o tema."""

    system_prompt = f"""Você é um jornalista esportivo profissional especializado no Flamengo,redator oficial do portal Fla10 News.

## DIRETRIZES EDITORIAIS OBRIGATÓRIAS:
{diretrizes}

## EXEMPLOS REAIS DO ESTILO FLA10 NEWS (use como referência de escrita):
{exemplos}

## REGRAS CRÍTICAS DE ESCRITA:
1. Parágrafos curtos (2-4 frases no máximo)
2. Subtítulos em negrito para dividir blocos
3. Linguagem jornalística moderna, direta e fluida
4. Contextualização antes de entrar no mérito
5. Análise tática quando aplicável
6. Uso de dados e estatísticas quando disponíveis
7. Referências históricas para enriquecer
8. Identidade rubro-negra presente (Rubro-Negro, Mengão, Mais Querido, Gávea)
9. NUNCA encerrar com perguntas ao leitor
10. Conclusão com interpretação e projeção
{fontes_section}
Escreva em português brasileiro. Mínimo de 2000 palavras com conteúdo denso, detalhado e bem fundamentado."""

    user_prompt = f"""Escreva uma matéria COMPLETA e DETALHADA para o Fla10 News seguindo EXATAMENTE o estilo editorial do portal.

IMPORTANTE: O artigo deve ter NO MÍNIMO 2000 palavras. Seja extremamente detalhado, desenvolvendo cada seção com profundidade.

NOTÍCIA BASE:
Título: {news_item['title']}
Resumo/Fonte: {news_item['summary']}

ESTRUTURA OBRIGATÓRIA (desenvolva CADA seção com MUITO detalhe):
1. Título H1 forte e pesquisável
2. Subtítulo contextualizado (em itálico abaixo do título)
3. Introdução objetiva (quem, o quê, quando, onde) - mínimo 200 palavras
4. Desenvolvimento em blocos com subtítulos H2/H3 (negrito) - mínimo 1200 palavras total:
   - Como foi o fato/partida (detalhe cada lance, momento, jogador)
   - Análise/Destaques (analise taticamente cada jogador, formação, jogadas)
   - Contexto e histórico (traga dados históricos, comparativos, estatísticas)
   - Impacto e consequências (analise o impacto no campeonato, no elenco, no clube)
   - Mercado da bola e perspectivas (se aplicável)
5. Conclusão editorial extensa (interpretação, projeção, leitura crítica) - mínimo 300 palavras

Se houver fontes adicionais fornecidas, use-as para enriquecer a matéria com dados, declarações e contexto extra.

FORMATO: Markdown
ESTILO: Idêntico aos exemplos reais do Fla10 News fornecidos
DESENVOLVIMENTO: Muito detalhado, com parágrafos ricos em informações"""

    try:
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4096,
            "top_p": 0.9
        }

        response = requests.post(
            NVIDIA_API_URL,
            headers=headers,
            json=payload,
            timeout=90
        )

        if response.status_code == 200:
            result = response.json()
            article = result["choices"][0]["message"]["content"]
            return article.strip()

        print(f"Erro API Nvidia: {response.status_code} - {response.text}")
        return create_fallback_article(news_item)

    except Exception as e:
        print(f"Erro na geração IA: {e}")
        return create_fallback_article(news_item)

def create_fallback_article(news_item):
    return f"""# {news_item['title']}

*{news_item.get('subtitle', 'Fla10 News')}*

**Fonte:** {news_item['source']}
**Publicado:** {news_item['published']}

## Resumo

{news_item['summary']}

---

*Artigo gerado automaticamente pelo Fla10 News*
"""

def fetch_url_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            from html.parser import HTMLParser
            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                    self.skip = False
                def handle_starttag(self, tag, attrs):
                    if tag in ['script', 'style', 'nav', 'header', 'footer']:
                        self.skip = True
                def handle_endtag(self, tag):
                    if tag in ['script', 'style', 'nav', 'header', 'footer']:
                        self.skip = False
                def handle_data(self, data):
                    if not self.skip:
                        text = data.strip()
                        if text:
                            self.text.append(text)
            extractor = TextExtractor()
            extractor.feed(response.text)
            content = ' '.join(extractor.text[:100])
            return content[:3000] if content else f"Conteúdo não extraído de: {url}"
        return f"Erro ao acessar: {url}"
    except Exception as e:
        return f"Erro ao acessar {url}: {str(e)[:100]}"

def generate_article_from_sources(fontes, info_adicionais=None, titulo_personalizado=None, model=DEFAULT_MODEL):
    diretrizes = load_file(DIRETRIZES_PATH)
    exemplos = load_file(EXEMPLOS_PATH)

    conteudo_fontes = []
    for i, url in enumerate(fontes, 1):
        conteudo = fetch_url_content(url)
        conteudo_fontes.append(f"--- FONTE {i}: {url} ---\n{conteudo}")

    fontes_conteudo = "\n\n".join(conteudo_fontes)

    info_section = ""
    if info_adicionais:
        info_section = f"""
## ⚠️ INSTRUÇÕES OBRIGATÓRIAS DO USUÁRIO (SEJA RIGOROSO EM SEGUIR):
O usuário forneceu as seguintes instruções que DEVEM ser seguidas EXATAMENTE na matéria:
---
{info_adicionais}
---
ESSAS INSTRUÇÕES SÃO PRIORIDADE MÁXIMA. A matéria DEVE seguir essas diretrizes em TODAS as seções.
Analise cada instrução e aplique na estrutura, foco, tom e conteúdo da matéria."""

    titulo_section = ""
    if titulo_personalizado:
        titulo_section = f"""
## TÍTULO SOLICITADO PELO USUÁRIO:
Use EXATAMENTE este título: {titulo_personalizado}"""

    system_prompt = f"""Você é um jornalista esportivo profissional especializado no Flamengo,redator oficial do portal Fla10 News.

## DIRETRIZES EDITORIAIS OBRIGATÓRIAS:
{diretrizes}

## EXEMPLOS REAIS DO ESTILO FLA10 NEWS (use como referência de escrita):
{exemplos}

## REGRAS CRÍTICAS DE ESCRITA:
1. Parágrafos curtos (2-4 frases no máximo)
2. Subtítulos em negrito para dividir blocos
3. Linguagem jornalística moderna, direta e fluida
4. Contextualização antes de entrar no mérito
5. Análise tática quando aplicável
6. Uso de dados e estatísticas quando disponíveis
7. Referências históricas para enriquecer
8. Identidade rubro-negra presente (Rubro-Negro, Mengão, Mais Querido, Gávea)
9. NUNCA encerrar com perguntas ao leitor
10. Conclusão com interpretação e projeção
{info_section}
Escreva em português brasileiro. Mínimo de 2000 palavras com conteúdo denso, detalhado e bem fundamentado."""

    user_prompt = f"""Escreva uma matéria COMPLETA e DETALHADA para o Fla10 News.

IMPORTANTE: O artigo deve ter NO MÍNIMO 2000 palavras. Seja extremamente detalhado.

## CONTEÚDO EXTRAÍDO DAS FONTES:
{fontes_conteudo}
{titulo_section}

## ⚠️ INSTRUÇÕES DO USUÁRIO QUE DEVEM SER SEGUIDAS RIGOROSAMENTE:
Se houver informações adicionais fornecidas acima (no system prompt), você DEVE segui-las em TODA a matéria.
Cada instrução do usuário deve ser aplicada na estrutura, foco e conteúdo do artigo.

ESTRUTURA OBRIGATÓRIA (desenvolva CADA seção com MUITO detalhe):
1. Título H1 forte e pesquisável (use o título personalizado se fornecido)
2. Subtítulo contextualizado (em itálico abaixo do título)
3. Introdução objetiva (quem, o quê, quando, onde) - mínimo 200 palavras
4. Desenvolvimento em blocos com subtítulos H2/H3 (negrito) - mínimo 1200 palavras total:
   - Resumo dos fatos principais
   - Análise detalhada (conforme instruções do usuário)
   - Contexto e histórico
   - Impacto e consequências
   - Perspectivas
5. Conclusão editorial extensa (interpretação, projeção, leitura crítica) - mínimo 300 palavras

Use TODAS as informações das fontes para criar uma matéria rica e detalhada.
SIGA RIGOROSAMENTE as instruções adicionais do usuário em TODAS as seções.

FORMATO: Markdown
ESTILO: Idêntico aos exemplos reais do Fla10 News fornecidos"""

    try:
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4096,
            "top_p": 0.9
        }

        response = requests.post(
            NVIDIA_API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            article = result["choices"][0]["message"]["content"]
            return article.strip()

        print(f"Erro API Nvidia: {response.status_code} - {response.text}")
        return f"Erro ao gerar matéria. Tente novamente."

    except Exception as e:
        print(f"Erro na geração IA: {e}")
        return f"Erro ao gerar matéria: {str(e)}"
