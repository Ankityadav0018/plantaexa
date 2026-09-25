# 🌿 Plantaexa — Plant Disease Recognition Chatbot

Plantaexa is an AI-powered plant disease recognition chatbot built with **Streamlit**.  
Upload a leaf image and get an instant disease diagnosis powered by a **ResNet50** deep learning model, with treatment recommendations from a curated disease database.

> **Text symptom analysis (BERT)** is optional — the app runs in image-only mode if the BERT model is not available.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🖼️ **Image Analysis** | Upload a leaf photo → ResNet50 identifies the disease (39 classes) |
| 💬 **Text Analysis** | Describe symptoms → BERT predicts the disease (7 classes) *(optional)* |
| 🎯 **Confidence Scores** | Color-coded confidence levels (High / Medium / Low) |
| 💊 **Treatment Recommendations** | Auto-maps predictions to symptoms & treatments from CSV database |
| 🎨 **Premium Chatbot UI** | Dark/light themes, glassmorphism, neon accents, micro-animations |
| 🐳 **Docker Support** | One-command deployment with docker-compose |

---

## 📁 Project Structure

```
plant_Doc_Bot-main/
├── chatbot/                   # ← Main Streamlit chatbot app
│   ├── app.py                 #   Entry point — run this with streamlit
│   ├── README.md              #   Chatbot-specific documentation
│   └── ui/
│       ├── components.py      #   UI components (header, chat messages, inputs)
│       └── styles.py          #   Custom CSS (dark/light themes, animations)
│
├── backend/                   # Shared ML backend
│   ├── config.py              #   Paths, labels, model settings
│   ├── models/
│   │   ├── image_model.py     #   ResNet50 image prediction pipeline
│   │   └── text_model.py      #   BERT text prediction pipeline (optional)
│   └── utils/
│       ├── disease_loader.py  #   Loads disease info indexed by label
│       └── treatment_lookup.py#   CSV-based treatment recommendations
│
├── data/                      # Model weights & dataset
│   ├── patched_model.keras    #   ResNet50 model (39 PlantVillage classes)
│   ├── plant_disease_dataset.csv  # Disease → symptoms & treatment database
│   └── PlantDoc-Dataset/      #   Image dataset (train/test splits)
│
├── scripts/                   # Utility scripts
│   ├── setup.sh               #   Environment setup helper
│   ├── run_tests.sh           #   Run test suite
│   └── clean_uploads.sh       #   Clear uploaded images
│
├── uploadimages/              # Temporary image upload directory
├── test_project.py            # Unit test suite
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container build instructions
├── docker-compose.yml         # Multi-service deployment
└── LICENSE                    # MIT License
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- `data/patched_model.keras` — ResNet50 model file (see [Model Downloads](#-model-downloads))
- `data/plant_disease_dataset.csv` — included in this repo
- *(Optional)* BERT model directory for text symptom analysis

### 1. Set Up Environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Chatbot

```bash
streamlit run chatbot/app.py
```

Open **http://localhost:8501** in your browser.

> **Image-only mode:** If the BERT model is not present, the app automatically runs in image-only mode and shows a notice. All image-based diagnosis features work normally.

### 3. Docker (Optional)

```bash
docker-compose up --build
```

Chatbot available at **http://localhost:8501**

---

## 🧠 Enabling Text Analysis (BERT)

The text symptom analysis feature requires a fine-tuned BERT model for sequence classification.

1. Place the BERT model files in:
   ```
   ~/Desktop/infosis/berth_model/
   ├── config.json
   ├── model.safetensors
   ├── tokenizer.json
   └── tokenizer_config.json
   ```

2. Restart the app — text mode will be automatically enabled.

**BERT predicts 7 disease classes:** Aphids, Blight, Downy Mildew, Leaf Spot, Powdery Mildew, Root Rot, Rust

---

## 🌾 Supported Crops & Diseases

The image model (ResNet50) recognizes **39 classes** across 14 crops:

| Crop | Diseases Detected |
|------|-------------------|
| Apple | Apple Scab, Black Rot, Cedar Apple Rust, Healthy |
| Blueberry | Healthy |
| Cherry | Powdery Mildew, Healthy |
| Corn | Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy |
| Grape | Black Rot, Esca (Black Measles), Leaf Blight, Healthy |
| Orange | Huanglongbing (Citrus Greening) |
| Peach | Bacterial Spot, Healthy |
| Pepper | Bacterial Spot, Healthy |
| Potato | Early Blight, Late Blight, Healthy |
| Raspberry | Healthy |
| Soybean | Healthy |
| Squash | Powdery Mildew |
| Strawberry | Leaf Scorch, Healthy |
| Tomato | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy |

---

## 🧪 Run Tests

```bash
python test_project.py
```

Tests cover: config imports, label format, CSV loading, treatment lookup, and image predictor label formatting.

---

## 📥 Model Downloads

| Model | Size | Link |
|-------|------|------|
| ResNet50 `patched_model.keras` | ~24 MB | [Google Drive](https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view?usp=sharing) |
| BERT text classifier | ~438 MB | Contact project maintainer |

Place the ResNet50 model at `data/patched_model.keras` inside the project directory.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

Built as part of the **Infosis Program** · © 2026 Plantaexa



