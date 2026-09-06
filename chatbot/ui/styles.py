"""
╔══════════════════════════════════════════════════════════════╗
║  Custom Styles – Dark & Light Theme for Streamlit            ║
╚══════════════════════════════════════════════════════════════╝

Supports both dark (default) and light themes.
Theme is toggled via session state and injected dynamically.
"""

import streamlit as st


def inject_custom_css():
    """Inject custom CSS based on the current theme."""
    theme = st.session_state.get("theme", "dark")

    # ── Shared base styles (both themes) ──
    base_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

    #MainMenu, footer, header { visibility: hidden !important; }

    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 900px !important;
    }

    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00c96a, #00b4d8) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        box-shadow: 0 4px 20px rgba(0, 201, 106, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #00c96a, #00b4d8) !important;
        border-radius: 8px !important;
    }

    /* Images */
    img { border-radius: 12px; }

    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }
    """

    if theme == "dark":
        theme_css = _dark_theme_css()
    else:
        theme_css = _light_theme_css()

    st.markdown(f"<style>{base_css}\n{theme_css}</style>", unsafe_allow_html=True)


def _dark_theme_css():
    """Premium dark glassmorphic theme."""
    return """
    /* ─── App Background ─── */
    .stApp { background: #050505 !important; }

    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }

    /* ─── Chat Messages ─── */
    div[data-testid="stChatMessage"] {
        background: rgba(20, 20, 20, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
    }

    /* ALL chat text → white */
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] div,
    div[data-testid="stChatMessage"] h1,
    div[data-testid="stChatMessage"] h2,
    div[data-testid="stChatMessage"] h3,
    div[data-testid="stChatMessage"] h4,
    div[data-testid="stChatMessage"] em {
        color: #ffffff !important;
    }

    div[data-testid="stChatMessage"] strong { color: #00FF87 !important; }

    /* Markdown text → white */
    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2,
    .stMarkdown h3, .stMarkdown h4, .stMarkdown span, .stMarkdown em {
        color: #ffffff !important;
    }
    .stMarkdown strong { color: #00FF87 !important; }

    /* Captions → muted */
    div[data-testid="stCaptionContainer"] p { color: #a1a1aa !important; }

    /* Progress bar text */
    .stProgress p { color: #a1a1aa !important; font-size: 0.82rem !important; }
    .stProgress > div { background: rgba(255,255,255,0.06) !important; border-radius: 8px !important; }

    /* HR */
    hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.06) !important; }
    div[data-testid="stChatMessage"] hr { border-top: 1px solid rgba(255,255,255,0.1) !important; }

    /* Text Input */
    .stTextInput > div > div > input {
        background: rgba(20, 20, 20, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        padding: 14px 20px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(0, 255, 135, 0.4) !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 135, 0.08) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #71717a !important; }

    /* File Uploader */
    section[data-testid="stFileUploader"] {
        background: rgba(20, 20, 20, 0.4) !important;
        border: 1px dashed rgba(255,255,255,0.1) !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }
    section[data-testid="stFileUploader"]:hover {
        border-color: rgba(0, 255, 135, 0.3) !important;
        background: rgba(0, 255, 135, 0.03) !important;
    }
    section[data-testid="stFileUploader"] label,
    section[data-testid="stFileUploader"] p,
    section[data-testid="stFileUploader"] span,
    section[data-testid="stFileUploader"] small { color: #a1a1aa !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 30, 30, 0.4) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
        color: #a1a1aa !important;
        padding: 10px 22px !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0, 255, 135, 0.08) !important;
        border-color: rgba(0, 255, 135, 0.3) !important;
        color: #00FF87 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0a0a0a !important;
        border-right: 1px solid rgba(255,255,255,0.04) !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] h5 { color: #e0e0e0 !important; }
    section[data-testid="stSidebar"] div[data-testid="stCaptionContainer"] p { color: #71717a !important; }

    /* Sidebar buttons (overrides gradient for delete/clear) */
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #e0e0e0 !important; font-weight: 500 !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,50,50,0.08) !important;
        border-color: rgba(255,50,50,0.3) !important;
        color: #ff6b6b !important; box-shadow: none !important;
    }

    /* Radio (theme toggle) */
    section[data-testid="stSidebar"] .stRadio label span { color: #e0e0e0 !important; }

    /* Chat image border */
    div[data-testid="stChatMessage"] img { border: 1px solid rgba(255,255,255,0.08); }

    /* Image captions */
    div[data-testid="stImage"] div[data-testid="stImageCaption"] {
        color: #71717a !important; font-size: 0.8rem !important;
    }

    /* Expander */
    .streamlit-expanderHeader { color: #e0e0e0 !important; }
    .streamlit-expanderContent { background: rgba(255,255,255,0.02) !important; border-radius: 8px !important; }
    details summary span { color: #e0e0e0 !important; }
    details div p, details div li { color: #c0c0c0 !important; }
    """


def _light_theme_css():
    """Clean, modern light theme."""
    return """
    /* ─── App Background ─── */
    .stApp { background: #f5f7fa !important; }

    ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 3px; }

    /* ─── Chat Messages ─── */
    div[data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e8ecf1 !important;
        border-radius: 16px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    }

    /* ALL chat text → dark */
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] div,
    div[data-testid="stChatMessage"] h1,
    div[data-testid="stChatMessage"] h2,
    div[data-testid="stChatMessage"] h3,
    div[data-testid="stChatMessage"] h4,
    div[data-testid="stChatMessage"] em {
        color: #1a1a2e !important;
    }

    div[data-testid="stChatMessage"] strong { color: #0a8754 !important; }

    /* Markdown → dark text */
    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2,
    .stMarkdown h3, .stMarkdown h4, .stMarkdown span, .stMarkdown em {
        color: #1a1a2e !important;
    }
    .stMarkdown strong { color: #0a8754 !important; }

    /* Captions */
    div[data-testid="stCaptionContainer"] p { color: #6b7280 !important; }

    /* Progress bar */
    .stProgress p { color: #6b7280 !important; font-size: 0.82rem !important; }
    .stProgress > div { background: #e8ecf1 !important; border-radius: 8px !important; }

    /* HR */
    hr { border: none !important; border-top: 1px solid #e8ecf1 !important; }
    div[data-testid="stChatMessage"] hr { border-top: 1px solid #e0e4ea !important; }

    /* Text Input */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 14px !important;
        color: #1a1a2e !important;
        padding: 14px 20px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #0a8754 !important;
        box-shadow: 0 0 0 2px rgba(10, 135, 84, 0.12) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #9ca3af !important; }

    /* File Uploader */
    section[data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 1px dashed #d1d5db !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }
    section[data-testid="stFileUploader"]:hover {
        border-color: #0a8754 !important;
        background: rgba(10, 135, 84, 0.02) !important;
    }
    section[data-testid="stFileUploader"] label,
    section[data-testid="stFileUploader"] p,
    section[data-testid="stFileUploader"] span,
    section[data-testid="stFileUploader"] small { color: #6b7280 !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background: #ffffff !important;
        border: 1px solid #e8ecf1 !important;
        border-radius: 10px !important;
        color: #6b7280 !important;
        padding: 10px 22px !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(10, 135, 84, 0.06) !important;
        border-color: #0a8754 !important;
        color: #0a8754 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e8ecf1 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] h5 { color: #1a1a2e !important; }
    section[data-testid="stSidebar"] div[data-testid="stCaptionContainer"] p { color: #9ca3af !important; }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: #f5f7fa !important;
        border: 1px solid #e8ecf1 !important;
        color: #374151 !important; font-weight: 500 !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(239,68,68,0.06) !important;
        border-color: rgba(239,68,68,0.3) !important;
        color: #dc2626 !important; box-shadow: none !important;
    }

    /* Radio (theme toggle) */
    section[data-testid="stSidebar"] .stRadio label span { color: #374151 !important; }

    /* Chat image border */
    div[data-testid="stChatMessage"] img { border: 1px solid #e8ecf1; }

    /* Image captions */
    div[data-testid="stImage"] div[data-testid="stImageCaption"] {
        color: #9ca3af !important; font-size: 0.8rem !important;
    }

    /* Expander */
    .streamlit-expanderHeader { color: #374151 !important; }
    .streamlit-expanderContent { background: #fafbfc !important; border-radius: 8px !important; }
    details summary span { color: #374151 !important; }
    details div p, details div li { color: #4b5563 !important; }

    /* Main button gradient override for light mode */
    .stButton > button { color: #ffffff !important; }
    """
