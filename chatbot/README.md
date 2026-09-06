# 🌿 Plantaexa — Unified Plant Disease Diagnostic Chatbot

A dual-AI chatbot system that integrates **ResNet50** (image classification) and **BERT** (text classification) models to diagnose plant diseases from leaf images or symptom descriptions.

> This is the Streamlit chatbot interface. For the Flask web app, see the [root README](../README.md).

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🖼️ **Image Analysis** | Upload a leaf photo → ResNet50 identifies the disease (39 classes) |
| 💬 **Text Analysis** | Describe symptoms → BERT predicts the disease (7 classes) |
| 🎯 **Confidence Scores** | Shows prediction confidence with visual indicators |
| 💊 **Treatment Recommendations** | Auto-maps diseases to treatments from the CSV database |
| 🗂️ **Chat History** | Maintains session-based conversation history |
| 🎨 **Premium UI** | Dark-themed, glassmorphic chatbot interface |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.9+
- All dependencies from root `requirements.txt`
- ResNet50 model at: `data/plant_disease_recog_resenet50_pwp.keras`
- BERT model at: `~/Desktop/infosis/berth_model/`
- CSV dataset at: `~/Desktop/infosis/berth_model/plant_disease_dataset_10000.csv`

### Steps

```bash
# From the project root (not chatbot/)
cd plantDoc

# Install dependencies
pip install -r requirements.txt

# Launch the chatbot
streamlit run chatbot/app.py
```

The app will open at **http://localhost:8501**

---

## 🧪 Run on Google Colab

```python
# ── Cell 1: Install Dependencies ──
!pip install streamlit tensorflow torch transformers safetensors Pillow

# ── Cell 2: Upload your model files ──
# Upload the following to Colab:
#   - plant_disease_recog_resenet50_pwp.keras
#   - berth_model/ folder (config.json, model.safetensors, tokenizer.json, tokenizer_config.json)
#   - plant_disease_dataset_10000.csv

# ── Cell 3: Clone/Upload the project code ──
# Upload the entire plantDoc/ directory to Colab

# ── Cell 4: Update paths in backend/config.py ──
# Edit backend/config.py to point to your Colab file paths:
#   RESNET_MODEL_PATH = "/content/data/plant_disease_recog_resenet50_pwp.keras"
#   BERT_MODEL_DIR = "/content/berth_model"
#   CSV_DATA_PATH = "/content/plant_disease_dataset_10000.csv"

# ── Cell 5: Run with localtunnel ──
!npm install -g localtunnel
!streamlit run /content/plantDoc/chatbot/app.py --server.port 8501 &
!lt --port 8501
```

---

## ⚙️ Configuration

All settings are centralized in **`backend/config.py`**:

| Setting | Description |
|---------|-------------|
| `RESNET_MODEL_PATH` | Path to the `.keras` model file |
| `BERT_MODEL_DIR` | Directory with BERT model files |
| `CSV_DATA_PATH` | Path to treatment CSV database |
| `IMAGE_LABELS` | 39 PlantVillage class labels |
| `BERT_LABEL_MAP` | Mapping of BERT output indices → disease names |
| `IMAGE_TARGET_SIZE` | Input image size (default: 160×160) |

### ⚠️ Important: BERT Label Mapping

The BERT model outputs labels 0–6. The mapping in `backend/config.py`:

```python
BERT_LABEL_MAP = {
    0: "Aphids",
    1: "Blight",
    2: "Downy Mildew",
    3: "Leaf Spot",
    4: "Powdery Mildew",
    5: "Root Rot",
    6: "Rust",
}
```

**If your training used a different label encoding order**, update this map to match your training notebook's `LabelEncoder` or `label2id` mapping.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              User Input                      │
│   ┌───────────┐      ┌───────────────┐      │
│   │  📷 Image │      │  💬 Text      │      │
│   └─────┬─────┘      └──────┬────────┘      │
│         │                   │                │
│         ▼                   ▼                │
│   ┌───────────┐      ┌───────────────┐      │
│   │ ResNet50  │      │    BERT       │      │
│   │ (160×160) │      │ (128 tokens)  │      │
│   └─────┬─────┘      └──────┬────────┘      │
│         │                   │                │
│         ▼                   ▼                │
│   ┌─────────────────────────────────┐       │
│   │      Disease Label              │       │
│   └──────────────┬──────────────────┘       │
│                  │                           │
│                  ▼                           │
│   ┌─────────────────────────────────┐       │
│   │  Treatment Lookup (CSV DB)      │       │
│   │  → Symptoms + Treatment        │       │
│   └──────────────┬──────────────────┘       │
│                  │                           │
│                  ▼                           │
│   ┌─────────────────────────────────┐       │
│   │  Unified Chat Response          │       │
│   └─────────────────────────────────┘       │
└─────────────────────────────────────────────┘
```

---

## 📄 License

MIT License — see [LICENSE](../LICENSE) for details.

Built as part of the Infosis program.
