

st.set_page_config(
    page_title="Fla10 News",
    page_icon="⚽",
    layout="wide"
)

os.makedirs(ARTICLES_DIR, exist_ok=True)

pagina = st.sidebar.radio(
    "Navegação",
    ["📝 Gerar de Notícias", "🔗 Gerar de Fontes", "📚 Artigos Salvos"]
)

if pagina == "📝 Gerar de Notícias":
    st.title("⚽ Fla10 News - Gerar de Notícias")
    st.markdown("Selecione notícias do RSS e gere artigos com IA")

    with st.sidebar:
        st.header("Controles")

        if st.button("🔄 Buscar Novas Notícias"):
            with st.spinner("Buscando notícias..."):
                news = get_flamengo_news()
                st.session_state['news'] = news
                st.session_state['selected'] = [False] * len(news)
                st.success(f"Encontradas {len(news)} notícias")

        if st.button("✅ Marcar Todas"):
            if 'news' in st.session_state:
                st.session_state['selected'] = [True] * len(st.session_state['news'])

        if st.button("❌ Desmarcar Todas"):
            if 'news' in st.session_state:
                st.session_state['selected'] = [False] * len(st.session_state['news'])

        if 'selected' in st.session_state:
            marcadas = sum(st.session_state['selected'])
            st.info(f"Marcadas: {marcadas}/{len(st.session_state['selected'])}")

        if st.button("📝 Gerar Artigos das Marcadas"):
            if 'news' in st.session_state and any(st.session_state['selected']):
                with st.spinner("Gerando artigos com IA..."):
                    articles = []
                    for i, news_item in enumerate(st.session_state['news']):
                        if st.session_state['selected'][i]:
                            article = generate_article_from_news(news_item)
                            articles.append({
                                'title': news_item['title'],
                                'content': article,
                                'generated_at': datetime.now().isoformat()
                            })
                    st.session_state['articles'] = articles
                    st.success(f"Gerados {len(articles)} artigos")
            else:
                st.warning("Marque pelo menos uma notícia")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📰 Notícias Encontradas")
        if 'news' in st.session_state and st.session_state['news']:
            for i, news in enumerate(st.session_state['news']):
                col_check, col_info = st.columns([0.1, 0.9])
                with col_check:
                    st.session_state['selected'][i] = st.checkbox(
                        "",
                        value=st.session_state['selected'][i],
                        key=f"check_{i}"
                    )
                with col_info:
                    with st.expander(f"{news['title'][:60]}..."):
                        st.write(f"**Título:** {news['title']}")
                        st.write(f"**Resumo:** {news['summary'][:300]}...")
                        st.write(f"**Fonte:** {news['source']}")
                        st.write(f"**Publicado:** {news['published']}")
        else:
            st.info("Clique em 'Buscar Novas Notícias' para iniciar")

    with col2:
        st.header("📝 Artigos Gerados")
        if 'articles' in st.session_state and st.session_state['articles']:
            for i, article in enumerate(st.session_state['articles']):
                with st.expander(f"Artigo {i+1}: {article['title'][:40]}..."):
                    st.markdown(article['content'])
                    if st.button(f"Salvar Artigo {i+1}", key=f"save_not_{i}"):
                        filename = f"artigo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                        filepath = os.path.join(ARTICLES_DIR, filename)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(f"# {article['title']}\n\n")
                            f.write(f"**Gerado em:** {article['generated_at']}\n\n")
                            f.write(article['content'])
                        st.success(f"Artigo salvo: {filepath}")
        else:
            st.info("Gere artigos selecionando notícias")

elif pagina == "🔗 Gerar de Fontes":
    st.title("🔗 Fla10 News - Gerar de Fontes")
    st.markdown("Crie matérias a partir de links de fontes na web")

    with st.sidebar:
        st.header("Fontes")
        st.markdown("Insira os links das notícias para base da matéria:")

        fontes = []
        for i in range(6):
            url = st.text_input(
                f"Fonte {i+1}",
                key=f"fonte_url_{i}",
                placeholder="https://exemplo.com/noticia...",
                label_visibility="collapsed"
            )
            if url:
                fontes.append(url)

        if fontes:
            st.success(f"{len(fontes)} fonte(s) adicionada(s)")

        st.markdown("---")
        st.header("📌 Informações Adicionais")
        info_adicionais = st.text_area(
            "Detalhes extras para a matéria:",
            key="info_adicionais",
            placeholder="Ex: Foco na análise tática, incluir declarações do treinador, comparar com temporada anterior...",
            height=150
        )

        st.markdown("---")

        titulo_personalizado = st.text_input(
            "Título personalizado (opcional)",
            key="titulo_custom",
            placeholder="Deixe vazio para a IA gerar automaticamente"
        )

        st.markdown("---")

        if st.button("📝 Gerar Matéria das Fontes"):
            if fontes:
                with st.spinner("Buscando conteúdo das fontes e gerando matéria..."):
                    article = generate_article_from_sources(
                        fontes=fontes,
                        info_adicionais=info_adicionais,
                        titulo_personalizado=titulo_personalizado
                    )
                    if 'articles_fontes' not in st.session_state:
                        st.session_state['articles_fontes'] = []
                    st.session_state['articles_fontes'].append({
                        'title': titulo_personalizado or "Matéria gerada de fontes",
                        'content': article,
                        'generated_at': datetime.now().isoformat(),
                        'fontes': fontes,
                        'info_adicionais': info_adicionais
                    })
                    st.success("Matéria gerada com sucesso!")
            else:
                st.warning("Adicione pelo menos uma fonte")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("🔗 Fontes Adicionadas")
        if fontes:
            for i, f_url in enumerate(fontes, 1):
                st.markdown(f"**{i}.** {f_url}")
        else:
            st.info("Adicione links de fontes na sidebar")

        if info_adicionais:
            st.markdown("---")
            st.header("📌 Informações Adicionais")
            st.markdown(info_adicionais)

    with col2:
        st.header("📝 Matérias Geradas")
        if 'articles_fontes' in st.session_state and st.session_state['articles_fontes']:
            for i, article in enumerate(st.session_state['articles_fontes']):
                with st.expander(f"Matéria {i+1}: {article['title'][:40]}...", expanded=True):
                    st.markdown(article['content'])

                    if article.get('fontes'):
                        st.markdown("**Fontes utilizadas:**")
                        for f_url in article['fontes']:
                            st.markdown(f"- {f_url}")

                    if article.get('info_adicionais'):
                        st.markdown("**Informações adicionais:**")
                        st.markdown(article['info_adicionais'])

                    if st.button(f"Salvar Matéria {i+1}", key=f"save_fonte_{i}"):
                        filename = f"materia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                        filepath = os.path.join(ARTICLES_DIR, filename)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(f"# {article['title']}\n\n")
                            f.write(f"**Gerado em:** {article['generated_at']}\n\n")
                            if article.get('fontes'):
                                f.write("**Fontes:**\n")
                                for f_url in article['fontes']:
                                    f.write(f"- {f_url}\n")
                                f.write("\n")
                            if article.get('info_adicionais'):
                                f.write(f"**Informações adicionais:**\n{article['info_adicionais']}\n\n")
                            f.write(article['content'])
                        st.success(f"Matéria salva: {filepath}")
        else:
            st.info("Gere matérias adicionando fontes e clicando em 'Gerar Matéria das Fontes'")

elif pagina == "📚 Artigos Salvos":
    st.title("📚 Artigos Salvos")

    arquivos = sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.md")), reverse=True)

    if arquivos:
        st.write(f"**Total de artigos:** {len(arquivos)}")

        for filepath in arquivos:
            filename = os.path.basename(filepath)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            mtime_str = mtime.strftime("%d/%m/%Y %H:%M")

            with open(filepath, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            titulo = conteudo.split('\n')[0].replace('# ', '') if conteudo else filename

            with st.expander(f"📄 {titulo[:70]}...", expanded=False):
                st.caption(f"Arquivo: `{filename}` | Salvo em: {mtime_str}")
                st.markdown(conteudo)

                col_del, col_dow = st.columns(2)
                with col_del:
                    if st.button(f"🗑️ Excluir", key=f"del_{filename}"):
                        os.remove(filepath)
                        st.success(f"Arquivo {filename} excluído")
                        st.rerun()
                with col_dow:
                    st.download_button(
                        label="⬇️ Download",
                        data=conteudo,
                        file_name=filename,
                        mime="text/markdown",
                        key=f"dl_{filename}"
                    )
    else:
        st.info("Nenhum artigo salvo ainda. Gere artigos nas páginas anteriores.")

st.markdown("---")
st.markdown("Desenvolvido com ❤️ para o Mengão")
