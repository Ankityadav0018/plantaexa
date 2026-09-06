"""
Plantaexa — Flask-based Plant Disease Recognition Server

Serves the single-page web UI where users upload leaf images
and receive AI-powered disease diagnoses via a ResNet50 model.
"""

import logging
import os
import uuid

import numpy as np
import tensorflow as tf
from flask import Flask, redirect, render_template, request, send_from_directory

from backend.config import CSV_DATA_PATH, IMAGE_TARGET_SIZE, RESNET_MODEL_PATH
from backend.utils.disease_loader import load_disease_data

# ─── Logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── Configuration ────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploadimages")

# ─── App Initialization ──────────────────────────────────────
app = Flask(__name__)

logger.info("Loading ResNet50 model from %s", RESNET_MODEL_PATH)
model = tf.keras.models.load_model(RESNET_MODEL_PATH)

logger.info("Loading disease data from CSV...")
plant_disease = load_disease_data(CSV_DATA_PATH)
logger.info("Loaded %d disease entries. Server ready.", len(plant_disease))


# ─── Routes ───────────────────────────────────────────────────
@app.route("/uploadimages/<path:filename>")
def uploaded_images(filename):
    """Serve previously uploaded images for result display."""
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/", methods=["GET"])
def home():
    """Render the main upload page."""
    return render_template("home.html")


@app.route("/upload/", methods=["POST", "GET"])
def upload_image():
    """Handle image upload, run prediction, and return results."""
    if request.method != "POST":
        return redirect("/")

    image = request.files["img"]
    filename = f"temp_{uuid.uuid4().hex}_{image.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    image.save(filepath)

    prediction = predict_disease(filepath)
    logger.info("Prediction: %s", prediction["name"])

    return render_template(
        "home.html",
        result=True,
        imagepath=f"/uploadimages/{filename}",
        prediction=prediction,
    )


# ─── Prediction Helpers ──────────────────────────────────────
def extract_features(image_path: str) -> np.ndarray:
    """Load and preprocess an image for model inference."""
    img = tf.keras.utils.load_img(image_path, target_size=IMAGE_TARGET_SIZE)
    arr = tf.keras.utils.img_to_array(img)
    return np.expand_dims(arr, axis=0)


def predict_disease(image_path: str) -> dict:
    """Run the ResNet50 model and return the matching disease info dict."""
    features = extract_features(image_path)
    prediction = model.predict(features, verbose=0)
    idx = int(prediction.argmax())
    return plant_disease[idx]


# ─── Entry Point ──────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    app.run(debug=True)