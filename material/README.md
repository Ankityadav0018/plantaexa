# 📚 Material

Reference materials, research papers, and project documentation.

## Contents

- Architecture diagrams
- Dataset documentation
- Model performance benchmarks
- Presentation slides
- Research paper references

## Key References

### PlantVillage Dataset
- **Source:** [PlantVillage on Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease)
- **Classes:** 39 plant disease categories
- **Images:** ~54,000 labeled leaf images

### Models Used

| Model | Architecture | Task | Input |
|-------|-------------|------|-------|
| ResNet50 | Residual Network (50 layers) | Image Classification | 160×160 RGB images |
| BERT | Bidirectional Encoder (Transformers) | Text Classification | 128-token symptom text |

### Disease Categories (BERT Text Model)

| # | Disease | Common Symptoms |
|---|---------|----------------|
| 0 | Aphids | Curled leaves, sticky residue, stunted growth |
| 1 | Blight | Brown/black lesions, rapid wilting |
| 2 | Downy Mildew | Yellow patches, fuzzy gray underside |
| 3 | Leaf Spot | Circular spots with dark borders |
| 4 | Powdery Mildew | White powdery coating on leaves |
| 5 | Root Rot | Wilting, yellowing, mushy roots |
| 6 | Rust | Orange/brown pustules on leaf underside |
