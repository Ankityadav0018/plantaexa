"""
╔══════════════════════════════════════════════════════════════╗
║  Plantaexa – Plant Disease Diagnostic Chatbot               ║
║  Powered by ResNet50 Deep Learning Image Classification      ║
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
    CSV_DATA_PATH,
    IMAGE_LABELS,
    PAGE_CONFIG,
    RESNET_MODEL_PATH,
)
from backend.models.image_model import ImagePredictor
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
def format_response(disease_name, confidence, treatment_info, source="ResNet50"):
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
        with st.spinner("🌿 Loading AI model... This may take a moment on first run."):
            try:
                image_predictor = load_image_model()
                treatment_db = load_treatment_db()
                st.session_state.models_loaded = True
            except Exception as e:
                st.error(f"❌ Failed to load model: {str(e)}")
                st.info(
                    "💡 Make sure the ResNet50 model file exists in data/ folder. "
                    "Check the README for setup instructions."
                )
                st.stop()
    else:
        image_predictor = load_image_model()
        treatment_db = load_treatment_db()

    render_sidebar()
    render_header()

    for msg in st.session_state.chat_history:
        render_chat_message(msg["role"], msg["content"], msg.get("extra"))

    uploaded_image = render_input_area()

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
                    disease_name, confidence, treatment_info, source="ResNet50"
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


if __name__ == "__main__":
    main()
