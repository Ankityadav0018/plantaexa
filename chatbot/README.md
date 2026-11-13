# 🌿 Plantaexa — Plant Disease Diagnostic Chatbot

A deep-learning powered chatbot system using **ResNet50** image classification to diagnose plant diseases from leaf photos and provide targeted treatment recommendations.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🖼️ **Image Analysis** | Upload a leaf photo → ResNet50 identifies the disease (39 classes) |
| 🎯 **Confidence Scores** | Shows prediction confidence with visual indicators |
| 💊 **Treatment Recommendations** | Auto-maps diseases to treatments from the CSV database |
| 🗂️ **Chat History** | Maintains session-based conversation history |
| 🎨 **Modern UI** | Clean, responsive Streamlit chatbot interface with Dark & Light theme |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.9+
- All dependencies from root `requirements.txt`
- Model file at: `data/patched_model.keras`
- CSV dataset at: `data/plant_disease_dataset.csv`

### Steps

```bash
# Activate environment
source .venv/bin/activate

# Launch the chatbot
streamlit run chatbot/app.py
```

The app will open at **http://localhost:8501**

---

## ⚙️ Configuration

All settings are centralized in **`backend/config.py`**:

| Setting | Description |
|---------|-------------|
| `RESNET_MODEL_PATH` | Path to the `.keras` model file |
| `CSV_DATA_PATH` | Path to treatment CSV database |
| `IMAGE_LABELS` | 39 PlantVillage class labels |
| `IMAGE_TARGET_SIZE` | Input image size (160×160) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│                 User Input                  │
│               ┌───────────┐                 │
│               │  📷 Image │                 │
│               └─────┬─────┘                 │
│                     │                       │
│                     ▼                       │
│               ┌───────────┐                 │
│               │ ResNet50  │                 │
│               │ (160×160) │                 │
│               └─────┬─────┘                 │
│                     │                       │
│                     ▼                       │
│        ┌─────────────────────────┐          │
│        │      Disease Label      │          │
│        └────────────┬────────────┘          │
│                     │                       │
│                     ▼                       │
│        ┌─────────────────────────┐          │
│        │ Treatment Lookup (CSV)  │          │
│        │ → Symptoms & Treatment  │          │
│        └────────────┬────────────┘          │
│                     │                       │
│                     ▼                       │
│        ┌─────────────────────────┐          │
│        │  Diagnostic Chat Output │          │
│        └─────────────────────────┘          │
└─────────────────────────────────────────────┘
```

---

## 📄 License

MIT License — see [LICENSE](../LICENSE) for details.
