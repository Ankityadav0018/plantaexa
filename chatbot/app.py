"""
╔══════════════════════════════════════════════════════════════╗
║  Plantaexa – Unified Plant Disease Diagnostic Chatbot       ║
║  Integrates ResNet50 (Image) + BERT (Text) Models           ║
║  Built with Streamlit for interactive chatbot-style UI       ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys

import streamlit as st

# Ensure project root is on the path for backend imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.config import (
    BERT_MODEL_DIR,
    CSV_DATA_PATH,
    IMAGE_LABELS,
    PAGE_CONFIG,
    RESNET_MODEL_PATH,
)
from backend.models.image_model import ImagePredictor
from backend.models.text_model import TextPredictor
from backend.utils.treatment_lookup import TreatmentLookup
from chatbot.ui.components import (
    render_chat_message,
    render_header,
    render_input_area,
    render_sidebar,
)
from chatbot.ui.styles import inject_custom_css

# ─── Page Configuration ───────────────────────────────────────
st.set_page_config(**PAGE_CONFIG)
inject_custom_css()


# ─── Model Loading (Cached) ──────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_image_model():
    """Load and cache the ResNet50 image classification model."""
    return ImagePredictor(RESNET_MODEL_PATH, IMAGE_LABELS)


@st.cache_resource(show_spinner=False)
def load_text_model():
    """Load and cache the BERT text classification model."""
    return TextPredictor(BERT_MODEL_DIR)


@st.cache_resource(show_spinner=False)
def load_treatment_db():
    """Load and cache the treatment recommendation database."""
    return TreatmentLookup(CSV_DATA_PATH)


# ─── Initialize Session State ────────────────────────────────
def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "models_loaded" not in st.session_state:
        st.session_state.models_loaded = False
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"


# ─── Response Formatter ──────────────────────────────────────
def format_response(disease_name, confidence, treatment_info, source):
    """Format a unified, user-friendly response string."""
    conf_pct = f"{confidence * 100:.1f}%"

    if confidence >= 0.8:
        conf_emoji, conf_label = "🟢", "High"
    elif confidence >= 0.5:
        conf_emoji, conf_label = "🟡", "Medium"
    else:
        conf_emoji, conf_label = "🔴", "Low"

    lines = [
        f"### 🌿 Disease Detected: **{disease_name}**",
        "",
        f"**Confidence:** {conf_emoji} {conf_pct} ({conf_label})",
        f"**Analysis Model:** {source}",
    ]

    if treatment_info:
        lines.extend([
            "",
            "---",
            "",
            f"🦠 **Symptoms:** {treatment_info.get('symptoms', 'N/A')}",
            "",
            f"💊 **Recommended Treatment:** {treatment_info.get('treatment', 'N/A')}",
        ])
        if treatment_info.get("plant_name"):
            lines.append(f"\n🌱 **Commonly Affects:** {treatment_info['plant_name']}")
    else:
        lines.extend([
            "",
            "---",
            "",
            "⚠️ No specific treatment data found in the database.",
            "Please consult a local agricultural expert.",
        ])

    return "\n".join(lines)


# ─── Main Application ────────────────────────────────────────
def main():
    init_session_state()

    if not st.session_state.models_loaded:
        with st.spinner("🌿 Loading AI models... This may take a moment on first run."):
            try:
                image_predictor = load_image_model()
                text_predictor = load_text_model()
                treatment_db = load_treatment_db()
                st.session_state.models_loaded = True
            except Exception as e:
                st.error(f"❌ Failed to load models: {str(e)}")
                st.info(
                    "💡 Make sure all model files are in the correct paths. "
                    "Check the README for setup instructions."
                )
                st.stop()
    else:
        image_predictor = load_image_model()
        text_predictor = load_text_model()
        treatment_db = load_treatment_db()

    render_sidebar()
    render_header()

    for msg in st.session_state.chat_history:
        render_chat_message(msg["role"], msg["content"], msg.get("extra"))

    text_input, uploaded_image = render_input_area()

    # ─── Process Image Input ──────────────────────────────
    if uploaded_image is not None:
        st.session_state.chat_history.append({
            "role": "user",
            "content": f"📷 Uploaded image: **{uploaded_image.name}**",
            "extra": {"type": "image", "image": uploaded_image},
        })

        with st.spinner("🔬 Analyzing leaf image with ResNet50..."):
            try:
                prediction = image_predictor.predict(uploaded_image)
                disease_name = prediction["label"]
                confidence = prediction["confidence"]
                treatment_info = treatment_db.lookup(disease_name)

                response_text = format_response(
                    disease_name, confidence, treatment_info, source="Image (ResNet50)"
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response_text,
                    "extra": {
                        "type": "prediction",
                        "disease": disease_name,
                        "confidence": confidence,
                        "treatment": treatment_info,
                        "model": "ResNet50",
                    },
                })
            except Exception as e:
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": f"❌ Image analysis failed: {str(e)}"}
                )

        st.rerun()

    # ─── Process Text Input ───────────────────────────────
    elif text_input:
        st.session_state.chat_history.append(
            {"role": "user", "content": text_input}
        )

        with st.spinner("🧠 Analyzing symptoms with BERT..."):
            try:
                prediction = text_predictor.predict(text_input)
                disease_name = prediction["label"]
                confidence = prediction["confidence"]
                treatment_info = treatment_db.lookup(disease_name)

                response_text = format_response(
                    disease_name, confidence, treatment_info, source="Text (BERT)"
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response_text,
                    "extra": {
                        "type": "prediction",
                        "disease": disease_name,
                        "confidence": confidence,
                        "treatment": treatment_info,
                        "model": "BERT",
                    },
                })
            except Exception as e:
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": f"❌ Text analysis failed: {str(e)}"}
                )

        st.rerun()


if __name__ == "__main__":
    main()
