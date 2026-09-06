"""
Plantaexa — Project Tests

Validates that all key components are importable and configured correctly.
"""

import os
import sys
import unittest

# Ensure project root is on the path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class TestConfig(unittest.TestCase):
    """Test that configuration loads correctly."""

    def test_config_imports(self):
        """Config module should be importable."""
        from backend.config import (
            BERT_LABEL_MAP,
            BERT_MODEL_DIR,
            CSV_DATA_PATH,
            IMAGE_LABELS,
            IMAGE_TARGET_SIZE,
            PAGE_CONFIG,
            RESNET_MODEL_PATH,
        )
        self.assertIsInstance(IMAGE_LABELS, list)
        self.assertEqual(len(IMAGE_LABELS), 39)
        self.assertIsInstance(BERT_LABEL_MAP, dict)
        self.assertEqual(len(BERT_LABEL_MAP), 7)
        self.assertEqual(IMAGE_TARGET_SIZE, (160, 160))

    def test_label_format(self):
        """All labels should follow the Plant___Disease format or single name."""
        from backend.config import IMAGE_LABELS
        for label in IMAGE_LABELS:
            self.assertIsInstance(label, str)
            self.assertGreater(len(label), 0)

    def test_bert_label_map_consistency(self):
        """BERT label map should have sequential indices starting from 0."""
        from backend.config import BERT_LABEL_MAP
        expected_keys = list(range(len(BERT_LABEL_MAP)))
        self.assertEqual(sorted(BERT_LABEL_MAP.keys()), expected_keys)


class TestDataPaths(unittest.TestCase):
    """Test that required data files exist."""

    def test_csv_exists(self):
        """CSV dataset should exist at the configured path."""
        from backend.config import CSV_DATA_PATH
        self.assertTrue(
            os.path.exists(CSV_DATA_PATH),
            f"CSV not found at: {CSV_DATA_PATH}",
        )

    def test_resnet_model_exists(self):
        """ResNet50 model file should exist."""
        from backend.config import RESNET_MODEL_PATH
        self.assertTrue(
            os.path.exists(RESNET_MODEL_PATH),
            f"ResNet model not found at: {RESNET_MODEL_PATH}",
        )

    def test_bert_model_dir_exists(self):
        """BERT model directory should exist."""
        from backend.config import BERT_MODEL_DIR
        self.assertTrue(
            os.path.isdir(BERT_MODEL_DIR),
            f"BERT model directory not found at: {BERT_MODEL_DIR}",
        )


class TestTreatmentLookup(unittest.TestCase):
    """Test the treatment lookup utility."""

    def setUp(self):
        from backend.config import CSV_DATA_PATH
        from backend.utils.treatment_lookup import TreatmentLookup
        self.lookup = TreatmentLookup(CSV_DATA_PATH)

    def test_diseases_loaded(self):
        """Should load at least one disease from the CSV."""
        diseases = self.lookup.get_all_diseases()
        self.assertGreater(len(diseases), 0)

    def test_known_disease_lookup(self):
        """Looking up 'Blight' should return a result."""
        result = self.lookup.lookup("Blight")
        self.assertIsNotNone(result)
        self.assertIn("symptoms", result)
        self.assertIn("treatment", result)

    def test_unknown_disease_returns_none(self):
        """Looking up a nonsense name should return None."""
        result = self.lookup.lookup("XYZ_nonexistent_disease_12345")
        self.assertIsNone(result)


class TestDiseaseLoader(unittest.TestCase):
    """Test the shared disease data loader."""

    def test_loads_39_entries(self):
        """Should return exactly 39 entries (one per IMAGE_LABELS)."""
        from backend.config import CSV_DATA_PATH
        from backend.utils.disease_loader import load_disease_data
        data = load_disease_data(CSV_DATA_PATH)
        self.assertEqual(len(data), 39)

    def test_entry_structure(self):
        """Each entry should have name, cause, cure keys."""
        from backend.config import CSV_DATA_PATH
        from backend.utils.disease_loader import load_disease_data
        data = load_disease_data(CSV_DATA_PATH)
        for entry in data:
            self.assertIn("name", entry)
            self.assertIn("cause", entry)
            self.assertIn("cure", entry)

    def test_healthy_plant_message(self):
        """Healthy labels should have a positive message."""
        from backend.config import CSV_DATA_PATH
        from backend.utils.disease_loader import load_disease_data
        data = load_disease_data(CSV_DATA_PATH)
        # Index 3 = Apple___healthy
        self.assertIn("healthy", data[3]["cure"].lower())


class TestImagePredictor(unittest.TestCase):
    """Test the image predictor utilities (no model load needed)."""

    def test_format_label_disease(self):
        """Should convert 'Apple___Black_rot' to 'Apple – Black Rot'."""
        from backend.models.image_model import ImagePredictor
        result = ImagePredictor._format_label("Apple___Black_rot")
        self.assertEqual(result, "Apple – Black Rot")

    def test_format_label_healthy(self):
        """Should convert 'Apple___healthy' to 'Apple – Healthy'."""
        from backend.models.image_model import ImagePredictor
        result = ImagePredictor._format_label("Apple___healthy")
        self.assertEqual(result, "Apple – Healthy")

    def test_format_label_no_separator(self):
        """Should handle labels without '___' separator."""
        from backend.models.image_model import ImagePredictor
        result = ImagePredictor._format_label("Background_without_leaves")
        self.assertEqual(result, "Background Without Leaves")


if __name__ == "__main__":
    unittest.main()
