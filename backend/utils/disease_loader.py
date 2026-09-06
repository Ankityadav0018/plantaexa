"""
╔══════════════════════════════════════════════════════════════╗
║  Disease Data Loader — CSV → Label-indexed Disease Info      ║
╚══════════════════════════════════════════════════════════════╝

Builds a list of disease info dicts (name, cause, cure)
indexed by the ResNet50 label order, using the CSV dataset.
"""

import csv
import os

from backend.config import IMAGE_LABELS

# ResNet label keywords → CSV disease name mapping
_KEYWORD_MAP = {
    "powdery_mildew": "Powdery Mildew",
    "blight": "Blight",
    "leaf_spot": "Leaf Spot",
    "rust": "Rust",
    "scab": "Leaf Spot",
    "black_rot": "Blight",
    "leaf_mold": "Downy Mildew",
    "septoria": "Leaf Spot",
    "spider_mite": "Aphids",
    "mosaic_virus": "Blight",
    "curl_virus": "Blight",
    "bacterial_spot": "Leaf Spot",
    "leaf_scorch": "Leaf Spot",
    "greening": "Root Rot",
    "measles": "Blight",
    "cercospora": "Leaf Spot",
}


def load_disease_data(csv_path: str) -> list[dict]:
    """
    Build a list of disease info dicts from the CSV, indexed by class label.

    Returns a list of 39 dicts (one per IMAGE_LABELS entry), each containing:
      - name: human-readable disease name (e.g. "Apple – Black Rot")
      - cause: symptoms / root cause text
      - cure: recommended treatment text

    Args:
        csv_path: Path to plant_disease_dataset_10000.csv
    """
    # Parse CSV into disease → {symptoms, treatment}
    disease_map: dict[str, dict] = {}
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                disease = row.get("Disease_Name", "").strip()
                if not disease:
                    continue
                if disease not in disease_map:
                    disease_map[disease] = {"symptoms": set(), "treatment": set()}
                disease_map[disease]["symptoms"].add(row.get("symptoms", "").strip())
                disease_map[disease]["treatment"].add(row.get("treatment", "").strip())

    # Build label-indexed list
    result = []
    for label in IMAGE_LABELS:
        parts = label.split("___")
        plant = parts[0].replace("_", " ") if parts else label
        disease_part = parts[1].replace("_", " ") if len(parts) == 2 else "Healthy"
        name = f"{plant} – {disease_part}"

        # Match label to CSV disease via keyword map
        matched = None
        label_lower = label.lower()
        for keyword, csv_disease in _KEYWORD_MAP.items():
            if keyword in label_lower:
                matched = disease_map.get(csv_disease)
                break

        if matched:
            cause = " | ".join(sorted(matched["symptoms"]))
            cure = " | ".join(sorted(matched["treatment"]))
        elif "healthy" in label_lower:
            cause = "No disease detected."
            cure = "Your plant looks healthy! Continue good agricultural practices."
        else:
            cause = "Refer to a local agricultural expert for diagnosis."
            cure = "Consult an agronomist for targeted treatment."

        result.append({"name": name, "cause": cause, "cure": cure})

    return result
