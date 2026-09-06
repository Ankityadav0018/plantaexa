# 📂 Data Directory

This directory stores trained model weights and datasets.

## Required Files

| File | Size | Source |
|------|------|--------|
| `plant_disease_recog_resenet50_pwp.keras` | ~250 MB | [Google Drive](https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view?usp=sharing) |
| `plant_disease_text_model.keras` | ~470 KB | Training notebook |

## External Files (Not in This Directory)

These files are stored externally and referenced via `backend/config.py`:

| File | Location | Size |
|------|----------|------|
| BERT model files | `~/Desktop/infosis/berth_model/` | ~438 MB |
| CSV dataset | `~/Desktop/infosis/berth_model/plant_disease_dataset_10000.csv` | ~880 KB |

> **Note:** Model files are excluded from Git via `.gitignore` due to their size.
> Download them separately or use Git LFS.
