"""
╔══════════════════════════════════════════════════════════════╗
║  Treatment Lookup – CSV-based Disease → Treatment Mapper     ║
╚══════════════════════════════════════════════════════════════╝

Parses the plant disease CSV dataset and provides lookup
functionality to map predicted diseases to treatments.
"""

import csv
import os
from collections import defaultdict


class TreatmentLookup:
    """Maps disease names to symptoms and treatment recommendations."""

    def __init__(self, csv_path: str):
        """
        Load treatment data from CSV file.

        Args:
            csv_path: Path to plant_disease_dataset_10000.csv
                      Columns: plant_type, plant_name, Disease_Name, symptoms, treatment
        """
        self.treatments = {}
        self._load_csv(csv_path)

    def _load_csv(self, csv_path: str):
        """Parse the CSV and build the treatment dictionary."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(
                f"Treatment database not found at: {csv_path}\n"
                "Please ensure the CSV file exists."
            )

        disease_data = defaultdict(
            lambda: {"symptoms": set(), "treatment": set(), "plants": set()}
        )

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                disease = row.get("Disease_Name", "").strip()
                if not disease:
                    continue

                data = disease_data[disease]
                data["symptoms"].add(row.get("symptoms", "").strip())
                data["treatment"].add(row.get("treatment", "").strip())
                plant = row.get("plant_name", "").strip()
                if plant:
                    data["plants"].add(plant)

        for disease, data in disease_data.items():
            self.treatments[disease.lower()] = {
                "disease_name": disease,
                "symptoms": " | ".join(sorted(data["symptoms"])) if data["symptoms"] else "N/A",
                "treatment": " | ".join(sorted(data["treatment"])) if data["treatment"] else "N/A",
                "plant_name": ", ".join(sorted(data["plants"])) if data["plants"] else None,
            }

    def lookup(self, disease_name: str) -> dict | None:
        """
        Look up treatment info for a given disease.

        Performs fuzzy matching: tries exact match first,
        then checks if the disease name contains any known disease.

        Args:
            disease_name: The predicted disease name

        Returns:
            dict with symptoms, treatment, plant_name or None
        """
        if not disease_name:
            return None

        name_lower = disease_name.lower().strip()

        # 1. Direct lookup
        if name_lower in self.treatments:
            return self.treatments[name_lower]

        # 2. Fuzzy: check if known disease name is contained within predicted label
        for key, value in self.treatments.items():
            if key in name_lower or name_lower in key:
                return value

        # 3. Try matching individual words
        words = name_lower.replace("–", " ").replace("-", " ").split()
        for word in words:
            if len(word) < 4:
                continue
            for key, value in self.treatments.items():
                if word in key:
                    return value

        # 4. Special mappings for ResNet50 labels → CSV diseases
        resnet_to_csv = {
            "powdery mildew": "powdery mildew",
            "blight": "blight",
            "leaf spot": "leaf spot",
            "rust": "rust",
            "scab": "leaf spot",
            "black rot": "blight",
            "leaf mold": "downy mildew",
            "septoria": "leaf spot",
            "spider mite": "aphids",
            "mosaic virus": "blight",
            "curl virus": "blight",
            "bacterial spot": "leaf spot",
            "leaf scorch": "leaf spot",
            "greening": "root rot",
            "measles": "blight",
            "cercospora": "leaf spot",
        }

        for pattern, mapped_disease in resnet_to_csv.items():
            if pattern in name_lower:
                return self.treatments.get(mapped_disease)

        return None

    def get_all_diseases(self) -> list:
        """Return a list of all known disease names."""
        return [v["disease_name"] for v in self.treatments.values()]
