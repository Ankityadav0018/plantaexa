"""
╔══════════════════════════════════════════════════════════════╗
║  Backend Configuration – Paths, Labels, and Settings         ║
╚══════════════════════════════════════════════════════════════╝
"""

import os

# ─── Base Paths ───────────────────────────────────────────────
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BACKEND_DIR)

# ─── Model Paths ─────────────────────────────────────────────
RESNET_MODEL_PATH = os.path.join(PROJECT_DIR, "data", "plant_disease_recog_resenet50_pwp.keras")

BERT_MODEL_DIR = os.path.join(
    os.path.expanduser("~"), "Desktop", "infosis", "berth_model"
)

# ─── Dataset Path ────────────────────────────────────────────
CSV_DATA_PATH = os.path.join(
    os.path.expanduser("~"), "Desktop", "infosis", "berth_model",
    "plant_disease_dataset_10000.csv",
)

# ─── Image Model Labels (39 PlantVillage classes) ────────────
IMAGE_LABELS = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Background_without_leaves",
    "Blueberry___healthy",
    "Cherry___Powdery_mildew",
    "Cherry___healthy",
    "Corn___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

# ─── BERT Disease Label Mapping (7 classes) ──────────────────
# Verified by running all 7 known symptom texts through the model.
# Each symptom maps to its correct disease at 100% confidence.
BERT_LABEL_MAP = {
    0: "Aphids",
    1: "Blight",
    2: "Downy Mildew",
    3: "Leaf Spot",
    4: "Powdery Mildew",
    5: "Root Rot",
    6: "Rust",
}

# ─── Image Preprocessing Config ──────────────────────────────
IMAGE_TARGET_SIZE = (160, 160)

# ─── Streamlit Page Config ────────────────────────────────────
PAGE_CONFIG = {
    "page_title": "Plantaexa — Plant Disease Chatbot",
    "page_icon": "🌿",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}
