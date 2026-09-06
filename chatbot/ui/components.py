"""
╔══════════════════════════════════════════════════════════════╗
║  UI Components – Streamlit Chat UI (Native API)              ║
╚══════════════════════════════════════════════════════════════╝

Uses Streamlit's native st.chat_message for reliable rendering.
Supports dark and light theme via session state toggle.
"""

import streamlit as st
from PIL import Image


def _get_theme_colors():
    """Return the correct color set based on current theme."""
    theme = st.session_state.get("theme", "dark")
    if theme == "dark":
        return {
            "title_color": "#ffffff",
            "subtitle_color": "#a1a1aa",
            "badge_bg": "rgba(0, 255, 135, 0.08)",
            "badge_border": "rgba(0, 255, 135, 0.25)",
            "badge_color": "#00FF87",
            "accent_from": "#00FF87",
            "accent_to": "#60EFFF",
            "card_bg": "rgba(0, 255, 135, 0.05)",
            "card_border_green": "rgba(0, 255, 135, 0.15)",
            "card_border_cyan": "rgba(96, 239, 255, 0.15)",
            "card_bg_cyan": "rgba(96, 239, 255, 0.05)",
            "card_text": "#ffffff",
            "card_muted": "#a1a1aa",
            "brand_color": "#ffffff",
        }
    else:
        return {
            "title_color": "#1a1a2e",
            "subtitle_color": "#6b7280",
            "badge_bg": "rgba(10, 135, 84, 0.06)",
            "badge_border": "rgba(10, 135, 84, 0.25)",
            "badge_color": "#0a8754",
            "accent_from": "#0a8754",
            "accent_to": "#0891b2",
            "card_bg": "rgba(10, 135, 84, 0.04)",
            "card_border_green": "rgba(10, 135, 84, 0.2)",
            "card_border_cyan": "rgba(8, 145, 178, 0.2)",
            "card_bg_cyan": "rgba(8, 145, 178, 0.04)",
            "card_text": "#1a1a2e",
            "card_muted": "#6b7280",
            "brand_color": "#1a1a2e",
        }


def render_header():
    """Render the hero/header section (theme-aware)."""
    c = _get_theme_colors()

    st.markdown(
        f"""
        <div style="text-align: center; padding: 1.5rem 0 0.5rem;">
            <div style="display: inline-flex; align-items: center; gap: 8px;
                        background: {c['badge_bg']}; 
                        border: 1px solid {c['badge_border']};
                        padding: 6px 18px; border-radius: 50px;
                        font-size: 0.78rem; font-weight: 600;
                        letter-spacing: 1.5px; text-transform: uppercase;
                        color: {c['badge_color']}; margin-bottom: 1rem;">
                <span style="width: 7px; height: 7px; background: {c['badge_color']};
                             border-radius: 50%; box-shadow: 0 0 8px {c['badge_color']};
                             display: inline-block;"></span>
                Dual-AI Diagnostics
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <h1 style="text-align: center; font-family: 'Outfit', sans-serif;
                   font-size: 3.2rem; font-weight: 800; letter-spacing: -1.5px;
                   line-height: 1.1; color: {c['title_color']}; margin: 0 0 0.3rem 0;">
            Plant health, powered by 
            <span style="background: linear-gradient(135deg, {c['accent_from']}, {c['accent_to']});
                         -webkit-background-clip: text; background-clip: text;
                         -webkit-text-fill-color: transparent;">AI.</span>
        </h1>
        <p style="text-align: center; font-size: 1.05rem; color: {c['subtitle_color']};
                  font-weight: 300; margin-bottom: 1.5rem;">
            Upload a leaf image or describe symptoms — our AI will diagnose instantly.
        </p>
        """,
        unsafe_allow_html=True,
    )


def render_chat_message(role: str, content: str, extra: dict = None):
    """
    Render a chat message using Streamlit's native chat_message API.
    """
    avatar = "👤" if role == "user" else "🌿"

    with st.chat_message(role, avatar=avatar):
        # Show uploaded image preview for user messages
        if extra and extra.get("type") == "image" and extra.get("image"):
            try:
                img_file = extra["image"]
                img_file.seek(0)
                img = Image.open(img_file)
                st.image(img, caption="Uploaded leaf image", width=250)
                img_file.seek(0)
            except Exception:
                st.caption("_(Image preview unavailable)_")

        # Render the text content
        if content:
            st.markdown(content)

        # Show confidence bar for assistant predictions
        if extra and extra.get("type") == "prediction":
            conf = extra.get("confidence", 0)
            model_name = extra.get("model", "AI")
            st.progress(conf, text=f"🎯 {model_name} Confidence: {conf*100:.1f}%")


def render_input_area():
    """
    Render the input area with text box and file uploader in tabs.
    """
    st.divider()

    tab_text, tab_image = st.tabs(["💬 Describe Symptoms", "📷 Upload Leaf Image"])

    text_input = None
    uploaded_image = None

    with tab_text:
        st.caption("Describe what you see on the plant leaves — discoloration, spots, wilting, etc.")

        text_val = st.text_input(
            "Symptom description",
            placeholder="e.g., Yellow patches on tomato leaves with white powder...",
            key="text_input_field",
            label_visibility="collapsed",
        )

        col1, col2 = st.columns([5, 1])
        with col2:
            text_submit = st.button(
                "Analyze 🧠", key="text_submit", use_container_width=True
            )

        if text_submit and text_val and text_val.strip():
            text_input = text_val.strip()

    with tab_image:
        st.caption("Upload a clear photo of the affected plant leaf (PNG, JPG).")

        uploaded_file = st.file_uploader(
            "Upload leaf image",
            type=["png", "jpg", "jpeg"],
            key="image_upload_field",
            label_visibility="collapsed",
        )

        if uploaded_file is not None:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                preview_img = Image.open(uploaded_file)
                st.image(preview_img, caption="Preview", use_container_width=True)
                uploaded_file.seek(0)

            col_a, col_b = st.columns([5, 1])
            with col_b:
                img_submit = st.button(
                    "Analyze 🔬", key="image_submit", use_container_width=True
                )

            if img_submit:
                uploaded_image = uploaded_file

    return text_input, uploaded_image


def render_sidebar():
    """Render the sidebar with theme toggle, model info, and controls."""
    c = _get_theme_colors()

    with st.sidebar:
        # ── Brand ──
        st.markdown(
            f"""
            <div style="text-align: center; padding: 1rem 0 0.5rem;">
                <h2 style="font-family: 'Outfit', sans-serif; font-weight: 800; 
                           letter-spacing: 2px; margin-bottom: 0; color: {c['brand_color']};">
                    Plantaexa<span style="background: linear-gradient(135deg, {c['accent_from']}, {c['accent_to']}); 
                    -webkit-background-clip: text; background-clip: text; 
                    -webkit-text-fill-color: transparent;">.AI</span>
                </h2>
                <p style="color: {c['card_muted']}; font-size: 0.8rem; margin-top: 4px;">
                    Unified Plant Disease Chatbot
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Theme Toggle ──
        st.markdown("##### 🎨 Appearance")

        current_theme = st.session_state.get("theme", "dark")

        theme_choice = st.radio(
            "Theme",
            options=["dark", "light"],
            index=0 if current_theme == "dark" else 1,
            format_func=lambda x: "🌙 Dark Mode" if x == "dark" else "☀️ Light Mode",
            key="theme_radio",
            label_visibility="collapsed",
            horizontal=True,
        )

        # Apply theme change
        if theme_choice != current_theme:
            st.session_state.theme = theme_choice
            st.rerun()

        st.divider()

        # ── Model Info ──
        st.markdown("##### 🤖 Active Models")

        st.markdown(
            f"""
            <div style="background: {c['card_bg']}; 
                        border: 1px solid {c['card_border_green']};
                        border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                <div style="font-size: 0.75rem; color: {c['accent_from']}; font-weight: 700; 
                            text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">
                    📷 Image Model
                </div>
                <div style="font-size: 0.95rem; color: {c['card_text']}; font-weight: 600;">ResNet50</div>
                <div style="font-size: 0.75rem; color: {c['card_muted']};">39 disease classes • PlantVillage</div>
            </div>
            <div style="background: {c['card_bg_cyan']}; 
                        border: 1px solid {c['card_border_cyan']};
                        border-radius: 10px; padding: 14px;">
                <div style="font-size: 0.75rem; color: {c['accent_to']}; font-weight: 700; 
                            text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">
                    💬 Text Model
                </div>
                <div style="font-size: 0.95rem; color: {c['card_text']}; font-weight: 600;">BERT (Transformers)</div>
                <div style="font-size: 0.75rem; color: {c['card_muted']};">7 disease classes • Symptom-based</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Chat Controls ──
        st.markdown("##### 🗂️ Chat Controls")

        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        chat_count = len(st.session_state.get("chat_history", []))
        st.caption(f"💬 {chat_count} messages in this session")

        st.divider()

        # ── Help ──
        with st.expander("💡 How to use", expanded=False):
            st.markdown(
                """
**Image Analysis (ResNet50):**
1. Click "📷 Upload Leaf Image" tab
2. Upload a clear leaf photo
3. Click **Analyze 🔬**

**Text Analysis (BERT):**
1. Click "💬 Describe Symptoms" tab
2. Type symptoms like *"white powder on leaves"*
3. Click **Analyze 🧠**
"""
            )

        with st.expander("📊 Supported Diseases", expanded=False):
            st.markdown(
                """
**BERT Text Model (7 classes):**
- Aphids · Blight · Downy Mildew
- Leaf Spot · Powdery Mildew
- Root Rot · Rust

**ResNet50 Image Model (39 classes):**
Apple Scab, Black Rot, Cedar Rust,
Powdery Mildew, Leaf Blight,
Bacterial Spot, and many more.
"""
            )
