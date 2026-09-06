# 🌿 Plantaexa — Plant Disease Recognition System

Plantaexa is an AI-powered plant disease recognition platform with two interfaces:

1. **Flask Web App** (`app.py`) — Upload a leaf image via a premium glassmorphic UI → instant diagnosis.
2. **Streamlit Chatbot** (`chatbot/app.py`) — Interactive dual-AI chatbot using ResNet50 (images) + BERT (text).

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🖼️ **Image Analysis** | Upload a leaf photo → ResNet50 identifies the disease (39 classes) |
| 💬 **Text Analysis** | Describe symptoms → BERT predicts the disease (7 classes) |
| 🎯 **Confidence Scores** | Visual confidence indicators with color-coded levels |
| 💊 **Treatment Recommendations** | Auto-maps predictions to treatments from CSV database |
| 🎨 **Premium UI** | Dark/light themes, glassmorphism, neon accents, micro-animations |
| 🐳 **Docker Support** | One-command deployment with docker-compose |

---

## 📁 Project Structure

```
plantDoc/
├── app.py                    # Flask web app (image upload & diagnosis)
├── test_project.py           # Project test suite
├── requirements.txt          # Python dependencies (all-in-one)
├── Dockerfile                # Container build instructions
├── docker-compose.yml        # Multi-service deployment
├── LICENSE                   # MIT License
├── README.md                 # This file
│
├── backend/                  # Shared ML backend code
│   ├── config.py             # Paths, labels, model settings
│   ├── models/
│   │   ├── image_model.py    # ResNet50 image prediction pipeline
│   │   └── text_model.py     # BERT text prediction pipeline
│   └── utils/
│       └── treatment_lookup.py  # CSV-based treatment recommendations
│
├── chatbot/                  # Streamlit dual-AI chatbot
│   ├── app.py                # Streamlit entry point
│   ├── README.md             # Chatbot-specific documentation
│   └── ui/
│       ├── styles.py         # Custom CSS (dark/light themes)
│       └── components.py     # UI components (header, chat, inputs)
│
├── data/                     # Model weights & datasets
│   ├── plant_disease_recog_resenet50_pwp.keras
│   └── plant_disease_text_model.keras
│
├── static/                   # Flask web assets
│   ├── css/style.css
│   ├── js/bootstrap.bundle.min.js
│   └── images/               # Backgrounds, logo
│
├── templates/                # Flask HTML templates
│   └── home.html
│
├── scripts/                  # Utility scripts
├── notebooks/                # Jupyter notebooks
├── material/                 # Reference materials
└── uploadimages/             # Temporary upload directory
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- Pre-trained models in `data/` directory
- BERT model files in `~/Desktop/infosis/berth_model/`
- CSV dataset at `~/Desktop/infosis/berth_model/plant_disease_dataset_10000.csv`

### Option 1: Flask Web App

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python app.py
```

Open **http://127.0.0.1:5000**

### Option 2: Streamlit Chatbot

```bash
source .venv/bin/activate
streamlit run chatbot/app.py
```

Open **http://localhost:8501**

### Option 3: Docker

```bash
docker-compose up --build
```

- Flask app → **http://localhost:5000**
- Chatbot → **http://localhost:8501**

---

## 🧪 Run Tests

```bash
python test_project.py
```

---

## 🛠️ Model Downloads

| Model | Size | Description |
|-------|------|-------------|
| [ResNet50 (.keras)](https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view?usp=sharing) | ~250 MB | 39 PlantVillage classes |
| BERT Model | ~438 MB | 7 disease classes (Aphids, Blight, Downy Mildew, Leaf Spot, Powdery Mildew, Root Rot, Rust) |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

Built as part of the Infosis program.
