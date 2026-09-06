"""
╔══════════════════════════════════════════════════════════════╗
║  Image Prediction Module – ResNet50 Pipeline                 ║
╚══════════════════════════════════════════════════════════════╝

Handles:
  - Loading the ResNet50 .keras model
  - Image preprocessing (resize, normalize)
  - Prediction with confidence scoring
"""

import io

import numpy as np
from PIL import Image

from backend.config import IMAGE_TARGET_SIZE


class ImagePredictor:
    """Wrapper for the ResNet50 plant disease image classifier."""

    def __init__(self, model_path: str, labels: list):
        """
        Initialize the image predictor.

        Args:
            model_path: Path to the .keras model file
            labels: List of class label strings (39 classes)
        """
        import tensorflow as tf

        self.model = tf.keras.models.load_model(model_path)
        self.labels = labels
        self.target_size = IMAGE_TARGET_SIZE

    def preprocess(self, image_file) -> np.ndarray:
        """
        Preprocess an uploaded image for model inference.

        Args:
            image_file: Streamlit UploadedFile or file-like object

        Returns:
            numpy array of shape (1, H, W, 3)
        """
        image_bytes = image_file.read()
        image_file.seek(0)

        img = Image.open(io.BytesIO(image_bytes))

        if img.mode != "RGB":
            img = img.convert("RGB")

        img = img.resize(self.target_size, Image.LANCZOS)

        img_array = np.array(img, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)

        return img_array

    def predict(self, image_file) -> dict:
        """
        Run disease prediction on an uploaded image.

        Args:
            image_file: Streamlit UploadedFile or file-like object

        Returns:
            dict with keys: 'label', 'confidence', 'top_predictions'
        """
        if image_file is None:
            raise ValueError("No image provided. Please upload a valid image file.")

        img_array = self.preprocess(image_file)
        predictions = self.model.predict(img_array, verbose=0)

        predicted_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_idx])

        raw_label = self.labels[predicted_idx]
        display_label = self._format_label(raw_label)

        top_indices = np.argsort(predictions[0])[::-1][:3]
        top_predictions = [
            {
                "label": self._format_label(self.labels[i]),
                "confidence": float(predictions[0][i]),
            }
            for i in top_indices
        ]

        return {
            "label": display_label,
            "raw_label": raw_label,
            "confidence": confidence,
            "top_predictions": top_predictions,
        }

    @staticmethod
    def _format_label(label: str) -> str:
        """
        Convert internal label to human-readable format.
        'Apple___Black_rot' → 'Apple – Black Rot'
        """
        parts = label.split("___")
        if len(parts) == 2:
            plant = parts[0].replace("_", " ").replace(",", ", ")
            disease = parts[1].replace("_", " ").title()
            return f"{plant} – {disease}"
        return label.replace("_", " ").title()
