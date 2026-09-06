"""
╔══════════════════════════════════════════════════════════════╗
║  Text Prediction Module – BERT Pipeline                      ║
╚══════════════════════════════════════════════════════════════╝

Handles:
  - Loading the BERT model from HuggingFace safetensors format
  - Text tokenization and preprocessing
  - Disease prediction from symptom descriptions
"""

import logging

import numpy as np

from backend.config import BERT_LABEL_MAP

logger = logging.getLogger(__name__)


class TextPredictor:
    """Wrapper for the BERT-based plant disease text classifier."""

    def __init__(self, model_dir: str):
        """
        Initialize the text predictor.

        Labels are resolved in this order:
          1. Model's own config.json id2label (if names aren't generic 'LABEL_N')
          2. Fallback to BERT_LABEL_MAP from backend/config.py

        Args:
            model_dir: Path to the directory containing:
                       - config.json
                       - model.safetensors
                       - tokenizer.json
                       - tokenizer_config.json
        """
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        import torch

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        logger.info("Loading BERT tokenizer from %s", model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)

        logger.info("Loading BERT model from %s", model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.model.to(self.device)
        self.model.eval()

        # Try to use the model's own id2label if it has real names
        model_labels = self.model.config.id2label
        has_real_names = model_labels and not all(
            v.startswith("LABEL_") for v in model_labels.values()
        )

        if has_real_names:
            self.label_map = {int(k): v for k, v in model_labels.items()}
            logger.info("Using model's id2label: %s", self.label_map)
        else:
            self.label_map = BERT_LABEL_MAP
            logger.info("Using config BERT_LABEL_MAP: %s", self.label_map)

        self.num_labels = len(self.label_map)

    def preprocess(self, text: str) -> dict:
        """
        Tokenize input text for BERT inference.

        Args:
            text: User's symptom description string

        Returns:
            dict of tokenized tensors ready for the model
        """
        import torch

        encoded = self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=128,
            return_tensors="pt",
        )

        return {k: v.to(self.device) for k, v in encoded.items()}

    def predict(self, text: str) -> dict:
        """
        Run disease prediction on symptom text.

        Args:
            text: User's text description of plant symptoms

        Returns:
            dict with keys: 'label', 'confidence', 'all_predictions'
        """
        import torch

        if not text or not text.strip():
            raise ValueError("Empty text input. Please describe the plant symptoms.")

        if len(text.strip()) < 5:
            raise ValueError(
                "Input too short. Please provide a more detailed description."
            )

        inputs = self.preprocess(text.strip())

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits

        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        probs_np = probabilities.cpu().numpy()[0]

        predicted_idx = int(np.argmax(probs_np))
        confidence = float(probs_np[predicted_idx])
        predicted_label = self.label_map.get(predicted_idx, f"Unknown (Label {predicted_idx})")

        all_predictions = [
            {
                "label": self.label_map.get(i, f"Label {i}"),
                "confidence": float(probs_np[i]),
            }
            for i in np.argsort(probs_np)[::-1]
        ]

        return {
            "label": predicted_label,
            "confidence": confidence,
            "all_predictions": all_predictions,
        }
