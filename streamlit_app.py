"""
Plantaexa — Streamlit-based Plant Disease Recognition UI

Modern interactive web interface for uploading leaf images
and receiving AI-powered disease diagnoses via a ResNet50 model.
"""

import logging
import os

import streamlit as st
import tensorflow as tf

from backend.config import CSV_DATA_PATH, IMAGE_LABELS, PAGE_CONFIG
from backend.models.image_model import ImagePredictor
from backend.utils.disease_loader import load_disease_data

# ─── Logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── Streamlit Page Configuration ──────────────────────────────
st.set_page_config(**PAGE_CONFIG)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        text-align: center;
        color: #2d7a2d;
        margin-bottom: 1rem;
    }
    .disease-container {
        background-color: #f0f8f0;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #2d7a2d;
    }
    .confidence-bar {
        margin: 1rem 0;
    }
    .healthy {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .diseased {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Session State Management ──────────────────────────────────
@st.cache_resource
def load_model_and_data():
    """Load the ResNet50 model and disease data once."""
    logger.info("Loading ResNet50 model...")
    model_path = os.path.join(
        os.path.dirname(__file__), "data", "plant_disease_recog_resenet50_pwp.keras"
    )
    
    logger.info("Loading disease data from CSV...")
    disease_data = load_disease_data(CSV_DATA_PATH)
    
    predictor = ImagePredictor(model_path, IMAGE_LABELS)
    logger.info("Model and disease data loaded successfully!")
    
    return predictor, disease_data


# ─── Main UI ──────────────────────────────────────────────────
def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🌿 Plantaexa — Plant Disease Recognition")
        st.markdown("*AI-Powered Leaf Disease Diagnosis*")
    
    st.divider()
    
    # Load model and data
    predictor, disease_data = load_model_and_data()
    
    # Tab layout
    tab1, tab2 = st.tabs(["📸 Disease Detection", "📚 About"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Upload Leaf Image")
            st.write("Upload a clear photo of a plant leaf for disease diagnosis.")
            
            uploaded_file = st.file_uploader(
                "Choose a leaf image...",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed"
            )
        
        with col2:
            st.subheader("Sample Images")
            st.info(
                "💡 **Tips for best results:**\n\n"
                "• Upload clear, well-lit leaf images\n"
                "• Avoid blurry or partially visible leaves\n"
                "• Show the affected area prominently\n"
                "• Use .jpg, .jpeg, or .png format"
            )
        
        st.divider()
        
        if uploaded_file is not None:
            st.subheader("Analysis Results")
            
            # Display uploaded image
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(uploaded_file, caption="Uploaded Leaf Image", use_column_width=True)
            
            # Run prediction
            with st.spinner("🔍 Analyzing leaf... Please wait..."):
                try:
                    prediction = predictor.predict(uploaded_file)
                    idx = IMAGE_LABELS.index(prediction["raw_label"])
                    disease_info = disease_data[idx]
                    
                    with col2:
                        # Disease name and confidence
                        confidence_pct = prediction["confidence"] * 100
                        
                        # Color based on health status
                        if "healthy" in prediction["raw_label"].lower():
                            st.success(f"✅ **{prediction['label']}**")
                            status_class = "healthy"
                            status_text = "Your plant appears healthy!"
                        else:
                            st.error(f"⚠️ **{prediction['label']}**")
                            status_class = "diseased"
                            status_text = "Disease detected. See treatment below."
                        
                        st.markdown(f"**Confidence:** {confidence_pct:.1f}%")
                        
                        # Confidence bar
                        st.progress(prediction["confidence"], text="Confidence Level")
                    
                    st.divider()
                    
                    # Disease Details
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("### 🔍 Disease Information")
                        st.markdown(f"**Name:** {disease_info['name']}")
                        st.markdown(f"**Cause/Symptoms:**\n\n{disease_info['cause']}")
                    
                    with col2:
                        st.markdown("### 🌱 Treatment & Care")
                        st.markdown(f"{disease_info['cure']}")
                    
                    st.divider()
                    
                    # Top predictions
                    st.markdown("### 🎯 Other Possible Diagnoses")
                    cols = st.columns(len(prediction["top_predictions"]))
                    
                    for i, (col, pred) in enumerate(zip(cols, prediction["top_predictions"])):
                        with col:
                            conf_pct = pred["confidence"] * 100
                            st.metric(
                                label=f"#{i+1}",
                                value=f"{conf_pct:.1f}%",
                                delta=pred["label"][:30] + "..." if len(pred["label"]) > 30 else pred["label"]
                            )
                
                except Exception as e:
                    st.error(f"❌ Error during prediction: {str(e)}")
                    logger.error(f"Prediction error: {e}")
    
    with tab2:
        st.markdown("### About Plantaexa")
        st.write(
            """
            **Plantaexa** is an advanced plant disease recognition system
            powered by deep learning and computer vision.
            
            #### 🎯 Features
            - **Real-time Disease Detection:** Instant leaf disease identification
            - **High Accuracy:** ResNet50 trained on 10,000+ labeled images
            - **Treatment Recommendations:** AI-powered treatment suggestions
            - **Multi-crop Support:** Recognizes 39 plant disease classes
            
            #### 🌾 Supported Crops
            Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper,
            Potato, Raspberry, Soybean, Squash, Strawberry, Tomato
            
            #### 📊 Model Details
            - **Architecture:** ResNet50 (Residual Neural Network)
            - **Training Data:** PlantVillage dataset (10,000+ images)
            - **Classes:** 39 (38 disease types + healthy)
            - **Accuracy:** ~95% on test set
            
            #### ⚠️ Disclaimer
            This tool is designed to assist farmers and agricultural professionals.
            For critical decisions, always consult with a qualified agronomist.
            """
        )
        
        st.markdown("---")
        st.markdown("**© 2026 Plantaexa — Infosis Program**")
        st.markdown("Licensed under MIT License")


if __name__ == "__main__":
    main()
