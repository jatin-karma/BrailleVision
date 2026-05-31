# Braille Dot Detection Dataset

## Overview
This dataset contains annotated images of Braille dots for training the YOLOv8 object detection model.

## Dataset Statistics
- **Total Images:** ~500
- **Total Annotations:** ~3000 bounding boxes
- **Image Format:** JPEG, PNG
- **Annotation Format:** YOLO (normalized coordinates)
- **Image Resolution:** Typically 640x480 to 1920x1080

## Dataset Splits
| Split | Images | Annotations | Purpose |
|-------|--------|-------------|---------|
| Train | ~400 | ~2400 | Model training |
| Validation | ~50 | ~300 | Hyperparameter tuning |
| Test | ~50 | ~300 | Final evaluation |

## Data Sources
1. **Roboflow Community Dataset** — Public Braille detection dataset
2. **Custom Collection** — Real embossed Braille samples collected by team
3. **Augmentation** — Additional samples generated via geometric and color augmentation

## Class Information
- **Single Class:** `dot`
- **Definition:** Individual raised dot on Braille surface
- **Characteristics:**
  - Raised physical dots (for embossed Braille)
  - Dark dots (for embossed/printed Braille)
  - Circular or slightly elliptical shape
  - Typically 2-4mm in diameter

## Annotation Details
- **Tool Used:** Roboflow
- **Annotation Format:** YOLO format (bounding boxes with normalized coordinates)
- **Coordinate System:** [x_center, y_center, width, height] (normalized 0-1)
- **File Structure:** Images and labels in parallel directories

## Data Augmentation Applied
- **Brightness:** ±20% variation
- **Saturation:** ±20% variation
- **Hue:** ±5% variation
- **Rotation:** ±15 degrees
- **Flip:** Horizontal flip (50% probability)
- **Blur:** Gaussian blur (kernel size 3-7)
- **Contrast:** ±25% variation

## File Structure
```
dataset/
├── data.yaml                 # YOLO dataset configuration
├── dataset_info.md          # This file
├── images/
│   ├── train/               # Training images (~400)
│   ├── val/                 # Validation images (~50)
│   └── test/                # Test images (~50)
└── labels/
    ├── train/               # Training annotations
    ├── val/                 # Validation annotations
    └── test/                # Test annotations
```

## Data Quality Notes
- ✅ All images manually reviewed for annotation correctness
- ✅ Balanced distribution across dataset splits
- ✅ Representative samples of various Braille grades and conditions
- ⚠️  Some images may have partial occlusion or shadows
- ⚠️  Lighting conditions vary to increase robustness

## Usage Guidelines
1. Load using Ultralytics: `YOLO("yolov8n.pt")` with `data=data.yaml`
2. Keep train/val/test splits as-is for reproducibility
3. For additional training, download and combine with similar datasets
4. Preprocessing (CLAHE, threshold) should be applied before inference

## Privacy & Ethics
- No personally identifiable information in dataset
- All Braille samples are public documents or team-owned materials
- Dataset used for accessibility improvement purposes
- No data shared with external parties without explicit permission

## Accessing the Dataset
- Full dataset available at: [Google Drive / Hugging Face link]
- Sample images available in `demo/screenshots/`
- For research use, contact: [your-email@example.com]

---

**Dataset Created:** 2026-05-31  
**Total Size:** ~500 MB (images + labels)  
**Format:** YOLO detection format  
**Recommended Citation:** TouchVision Team (2026), Braille Dot Detection Dataset
