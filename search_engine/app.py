import streamlit as st
import streamlit.components.v1 as components
from engine.preprocessor import preprocess
from engine.loader import load_documents
from engine.indexer import build_index, search_query
from engine.ranker import rank_results

st.set_page_config(
    page_title="DocSearch",
    page_icon="✨",
    layout="wide"
)

@st.cache_resource
def load_engine():
    raw_docs = load_documents("documents")
    processed_docs = {name: preprocess(text) for name, text in raw_docs.items()}
    index = build_index(processed_docs)
    return index, raw_docs

index, raw_docs = load_engine()

# ── Inject a tiny JS that sets dark/light on the PARENT page immediately ──
st.markdown("""
<script>
(function() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const root = document.documentElement;
    root.style.setProperty('--header-title-color', isDark ? '#C8B6FF' : '#7C5CFF');
    root.style.setProperty('--header-sub-color',   isDark ? '#A0A0CC' : '#8A8AAD');
    root.style.setProperty('--page-bg',            isDark ? '#0F0F1A' : '#F9F7FF');
    root.style.setProperty('--page-text',          isDark ? '#E0E0FF' : '#1F1F3A');
    document.body.style.backgroundColor = isDark ? '#0F0F1A' : '#F9F7FF';
    document.body.style.color           = isDark ? '#E0E0FF' : '#1F1F3A';

    // Watch for OS theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        const d = e.matches;
        root.style.setProperty('--header-title-color', d ? '#C8B6FF' : '#7C5CFF');
        root.style.setProperty('--header-sub-color',   d ? '#A0A0CC' : '#8A8AAD');
        document.body.style.backgroundColor = d ? '#0F0F1A' : '#F9F7FF';
        document.body.style.color           = d ? '#E0E0FF' : '#1F1F3A';
    });
})();
</script>
<style>
:root {
    --header-title-color: #7C5CFF;
    --header-sub-color:   #8A8AAD;
}
</style>
<div style="text-align:center; margin: 2.5rem 0 2rem;">
    <h1 style="font-family:'Syne',sans-serif; font-weight:800; color:var(--header-title-color); font-size:2.8rem; margin-bottom:0.6rem;">
        ✨ DocSearch
    </h1>
    <p style="color:var(--header-sub-color); font-size:1.15rem; max-width:580px; margin:0 auto;">
        Find anything in your documents — beautifully.
    </p>
</div>
""", unsafe_allow_html=True)

query = st.text_input(
    "",
    placeholder="Search through your documents…",
    key="search_input",
    help="Try keywords, phrases, titles — anything!"
)

if query:
    scores = search_query(index, query)
    results = rank_results(scores) if isinstance(scores, dict) else scores
    results = results[:12]
else:
    results = []

def highlight(text: str, query: str) -> str:
    if not query:
        return text[:280] + ("…" if len(text) > 280 else "")
    words = set(preprocess(query))
    snippet = text[:280] + ("…" if len(text) > 280 else "")
    for word in words:
        for variant in {word, word.capitalize(), word.upper()}:
            if variant in snippet:
                snippet = snippet.replace(variant, f"<mark>{variant}</mark>")
    return snippet

def build_results_html(results, query, raw_docs):
    if not query:
        chips = "".join([
            f'<span class="chip">{name}</span>'
            for name in sorted(raw_docs.keys())[:10]
        ])
        return f"""
        <div class="empty-state idle">
            <div class="icon-big">🔍</div>
            <h3>Ready when you are</h3>
            <p>Your documents are lovingly indexed.<br>Just type to discover ✨</p>
            <div class="chip-container">{chips}</div>
        </div>"""

    if not results:
        return f"""
        <div class="empty-state">
            <div class="icon-big">🥀</div>
            <h3>No matches found</h3>
            <p>We couldn't find anything for "<strong>{query}</strong>".<br>Try another word or phrase?</p>
        </div>"""

    max_score = max(s for _, s in results) if results else 1
    cards = ""
    for doc_name, score in results:
        snippet = highlight(raw_docs.get(doc_name, ""), query)
        rel_pct = round((score / max_score) * 100)
        cards += f"""
        <div class="result-card">
            <div class="card-header">
                <div class="doc-info">
                    <div class="doc-icon">📄</div>
                    <div>
                        <div class="doc-title">{doc_name}</div>
                        <div class="doc-path">documents / {doc_name}</div>
                    </div>
                </div>
                <div class="score-pill">{rel_pct}% · {score:.2f}</div>
            </div>
            <div class="snippet">{snippet}</div>
        </div>"""

    return f"""
    <div class="results-meta">
        <div><strong>{len(results)}</strong> result{'s' if len(results) != 1 else ''} for "{query}"</div>
        <div>Sorted by relevance</div>
    </div>""" + cards


# ── Build HTML with theme baked in via JS ──
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Syne:wght@700;800&display=swap" rel="stylesheet"/>
<style>
    :root {{
        --primary:         #7C5CFF;
        --accent:          #FF6B9A;
        --highlight-light: #FFE4F0;
        --highlight-dark:  #4A2A5A;
        --radius:          18px;

        /* Light defaults */
        --bg-start:    #F9F7FF;
        --bg-end:      #F1F4FF;
        --card:        #FFFFFF;
        --border:      #E8E6FF;
        --text:        #1F1F3A;
        --muted:       #6B6B8A;
        --snippet:     #2f2f4a;
        --shadow-sm:   0 8px 24px rgba(124,92,255,0.10);
        --shadow-md:   0 14px 40px rgba(124,92,255,0.16);
        --score-bg:    linear-gradient(135deg,#fff0f5,#ffe4f0);
        --score-text:  #d4417a;
        --icon-bg:     linear-gradient(135deg,#f0eaff,#e6deff);
        --chip-bg:     #ffffff;
        --chip-border: #e6e3ff;
        --chip-text:   #5a5a7e;
        --empty-icon:  #b19dff;
        --mark-bg:     #FFE4F0;
    }}

    body {{
        font-family: 'DM Sans', system-ui, sans-serif;
        background: linear-gradient(180deg, var(--bg-start) 0%, var(--bg-end) 100%);
        color: var(--text);
        line-height: 1.6;
        padding: 2rem 1.5rem;
        min-height: 100vh;
        margin: 0;
        transition: background 0.4s ease, color 0.4s ease;
    }}

    /* ── Result cards ── */
    .results-meta {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0 1.2rem;
        font-size: 0.98rem;
        color: var(--muted);
        font-weight: 500;
    }}
    .result-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.24s ease;
        position: relative;
        overflow: hidden;
    }}
    .result-card:hover {{
        transform: translateY(-6px);
        box-shadow: var(--shadow-md);
        border-color: #d4ccff;
    }}
    .result-card::before {{
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 5px;
        background: linear-gradient(180deg, var(--primary), var(--accent));
        opacity: 0.82;
    }}
    .card-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 0.9rem;
    }}
    .doc-info {{
        display: flex;
        align-items: center;
        gap: 0.9rem;
        flex: 1;
    }}
    .doc-icon {{
        width: 44px; height: 44px;
        background: var(--icon-bg);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem;
        flex-shrink: 0;
    }}
    .doc-title {{
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1.18rem;
        color: var(--primary);
        margin-bottom: 0.2rem;
    }}
    .doc-path {{ font-size: 0.84rem; color: var(--muted); }}
    .score-pill {{
        background: var(--score-bg);
        color: var(--score-text);
        font-size: 0.86rem;
        font-weight: 600;
        padding: 0.42rem 0.9rem;
        border-radius: 2rem;
        white-space: nowrap;
    }}
    .snippet {{ font-size: 0.96rem; color: var(--snippet); }}
    mark {{
        background: var(--mark-bg);
        color: var(--primary);
        padding: 0.12em 0.28em;
        border-radius: 4px;
        font-weight: 500;
    }}

    /* ── Empty/idle ── */
    .empty-state {{
        text-align: center;
        padding: 6rem 1.5rem 4rem;
        color: var(--muted);
    }}
    .icon-big {{
        font-size: 4.2rem;
        margin-bottom: 1.4rem;
        opacity: 0.92;
    }}
    .empty-state h3 {{
        font-family: 'Syne', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.9rem;
        color: var(--text);
    }}
    .empty-state p {{ color: var(--muted); }}
    .chip-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
        justify-content: center;
        margin-top: 1.8rem;
        max-width: 720px;
        margin-left: auto;
        margin-right: auto;
    }}
    .chip {{
        background: var(--chip-bg);
        border: 1px solid var(--chip-border);
        border-radius: 2rem;
        padding: 0.5rem 1.1rem;
        font-size: 0.88rem;
        color: var(--chip-text);
    }}
</style>

<script>
    function setTheme() {{
        // Read Streamlit's theme from the parent page's data attribute
        let isDark = false;
        try {{
            const parent = window.parent.document;
            const html = parent.documentElement;
            // Streamlit sets data-theme="dark" or "light" on the html element
            const streamlitTheme = html.getAttribute('data-theme');
            if (streamlitTheme) {{
                isDark = streamlitTheme === 'dark';
            }} else {{
                // Fallback: check background brightness
                const bg = window.getComputedStyle(parent.body).backgroundColor;
                const rgb = bg.match(/\d+/g);
                if (rgb) {{
                    const brightness = (parseInt(rgb[0])*299 + parseInt(rgb[1])*587 + parseInt(rgb[2])*114) / 1000;
                    isDark = brightness < 128;
                }}
            }}
        }} catch(e) {{
            // Cross-origin fallback to OS preference
            isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        }}

        const root = document.documentElement;

        if (isDark) {{
            root.style.setProperty('--bg-start',    '#0F0F1A');
            root.style.setProperty('--bg-end',      '#141424');
            root.style.setProperty('--card',        '#181824');
            root.style.setProperty('--border',      '#2A2A44');
            root.style.setProperty('--text',        '#E0E0FF');
            root.style.setProperty('--muted',       '#A0A0CC');
            root.style.setProperty('--snippet',     '#C8C8E8');
            root.style.setProperty('--score-bg',    'linear-gradient(135deg,#3A1A2F,#2E1438)');
            root.style.setProperty('--score-text',  '#FFB3D9');
            root.style.setProperty('--icon-bg',     'linear-gradient(135deg,#2A1F44,#352A55)');
            root.style.setProperty('--chip-bg',     '#1E1E38');
            root.style.setProperty('--chip-border', '#3A3A60');
            root.style.setProperty('--chip-text',   '#C0B0FF');
            root.style.setProperty('--empty-icon',  '#A78BFA');
            root.style.setProperty('--mark-bg',     '#4A2A5A');
            root.style.setProperty('--primary',     '#C8B6FF');
        }} else {{
            root.style.setProperty('--bg-start',    '#F9F7FF');
            root.style.setProperty('--bg-end',      '#F1F4FF');
            root.style.setProperty('--card',        '#FFFFFF');
            root.style.setProperty('--border',      '#E8E6FF');
            root.style.setProperty('--text',        '#1F1F3A');
            root.style.setProperty('--muted',       '#6B6B8A');
            root.style.setProperty('--snippet',     '#2f2f4a');
            root.style.setProperty('--score-bg',    'linear-gradient(135deg,#fff0f5,#ffe4f0)');
            root.style.setProperty('--score-text',  '#d4417a');
            root.style.setProperty('--icon-bg',     'linear-gradient(135deg,#f0eaff,#e6deff)');
            root.style.setProperty('--chip-bg',     '#ffffff');
            root.style.setProperty('--chip-border', '#e6e3ff');
            root.style.setProperty('--chip-text',   '#5a5a7e');
            root.style.setProperty('--empty-icon',  '#b19dff');
            root.style.setProperty('--mark-bg',     '#FFE4F0');
            root.style.setProperty('--primary',     '#7C5CFF');
        }}
    }}

    // Run immediately and re-check every second to catch Streamlit theme changes
    setTheme();
    setInterval(setTheme, 1000);
</script>
</head>
<body>
    {build_results_html(results, query, raw_docs)}
</body>
</html>
"""

components.html(html_content, height=740, scrolling=True)