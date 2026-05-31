# 🎯 Complete Guide: Download Dataset from Google Drive & Generate Training Metrics

This guide will help you:
1. Download your Braille dataset from Google Drive
2. Organize it properly for YOLO training
3. Generate confusion matrix, metrics, and all visualizations

---

## 🔗 Your Google Drive Dataset Link

**⚠️ IMPORTANT: Add your Google Drive link here:**

```
YOUR_DATASET_GOOGLE_DRIVE_LINK: [PASTE YOUR LINK HERE]
```

**Example format:**
```
https://drive.google.com/drive/folders/1aB2cD3eF4gH5iJ6kL7mN8oP9qR0sT1uV
```

**How to get your link:**
1. Open Google Drive and find your TouchVision dataset folder
2. Right-click the folder
3. Select "Get link"
4. Copy the link (should look like: `https://drive.google.com/drive/folders/...`)
5. Paste it in the placeholder above
6. Make sure the link is **shared** (at least "Viewer" access)

---

## Step 1: Download Dataset from Google Drive

### Option A: Download Entire Folder (Recommended)

1. **Open Google Drive:** https://drive.google.com
2. **Find your TouchVision dataset folder** (from your Colab training)
3. **Right-click the folder** → Select **"Download"**
4. **Browser downloads it as ZIP** (may take 5-10 minutes for large datasets)
5. **Extract ZIP** to your local machine

### Option B: Download Individual Folders

If the full folder is too large:

1. Download `images/train/` folder
2. Download `images/val/` folder
3. Download `images/test/` folder (if exists)
4. Download `labels/train/` folder
5. Download `labels/val/` folder
6. Download `labels/test/` folder (if exists)

### Option C: Use Google Colab to Download (Fastest for Large Datasets)

```python
# In Google Colab, run this to download your dataset:
from google.colab import files
import shutil
import os

# Zip your dataset
shutil.make_archive('braille_dataset', 'zip', '/path/to/your/dataset')

# Download
files.download('braille_dataset.zip')
```

---

## Step 2: Organize Dataset Locally

### Expected Directory Structure:

```
d:/TouchVision/dataset/
├── data.yaml                    ← Already have this
├── images/
│   ├── train/                   ← YOLO format images
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── val/
│   │   ├── image1.jpg
│   │   └── ...
│   └── test/
│       └── ...
└── labels/
    ├── train/                   ← YOLO format labels (.txt files)
    │   ├── image1.txt
    │   ├── image2.txt
    │   └── ...
    ├── val/
    │   ├── image1.txt
    │   └── ...
    └── test/
        └── ...
```

### Steps:

1. **Extract your downloaded ZIP file**
2. **Copy the `images` and `labels` folders** into `d:/TouchVision/dataset/`
3. **Verify structure:**
   ```bash
   cd d:/TouchVision/dataset
   dir images/train    # Should show JPG/PNG files
   dir labels/train    # Should show .txt files
   ```

---

## Step 3: Run Training to Generate Metrics

### Option A: Automatic Setup (Recommended)

```bash
cd d:/TouchVision
python setup_training_env.py
```

This script will:
- ✓ Verify dataset structure
- ✓ Check all configurations
- ✓ Run YOLO training
- ✓ Generate confusion matrix, curves, metrics
- ✓ Copy results to `training/results/`
- ✓ Update `model/best.pt`

### Option B: Manual YOLO Training Command

```bash
cd d:/TouchVision

# Run training
yolo detect train \
  data=dataset/data.yaml \
  model=yolov8n.pt \
  epochs=100 \
  imgsz=640 \
  batch=16 \
  patience=20 \
  name=braille_dot_detector \
  device=0
```

**Parameter Explanation:**
- `data=dataset/data.yaml` - Dataset config file
- `model=yolov8n.pt` - YOLOv8 Nano (smallest & fastest)
- `epochs=100` - Number of training iterations
- `imgsz=640` - Input image size
- `batch=16` - Batch size (reduce to 8 if out of memory)
- `patience=20` - Early stopping if no improvement
- `device=0` - GPU 0 (use `device=cpu` for CPU training)

### Option C: If Using Google Colab Again (Alternative)

You can re-run training on Google Colab and download results:

```python
# In Google Colab notebook:

# Mount drive
from google.colab import drive
drive.mount('/content/drive')

# Install YOLOv8
!pip install ultralytics

# Train
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model.train(
    data='/content/drive/MyDrive/TouchVision/dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    patience=20,
    device=0,
    plots=True
)

# Zip results for download
import shutil
shutil.make_archive('training_results', 'zip', 'runs/detect/braille_dot_detector')

# Download
from google.colab import files
files.download('training_results.zip')
```

---

## Step 4: What You'll Get After Training

### 📊 Generated Files:

```
runs/detect/braille_dot_detector/
├── weights/
│   ├── best.pt              ← Best model (use this!)
│   └── last.pt              ← Last checkpoint
├── confusion_matrix.png     ← Validation confusion matrix
├── precision_curve.png      ← Precision vs confidence
├── recall_curve.png         ← Recall vs confidence
├── F1_curve.png             ← F1 vs confidence
├── P_curve.png              ← Precision vs epoch
├── R_curve.png              ← Recall vs epoch
├── results.csv              ← Epoch-wise metrics
└── args.yaml                ← Training arguments
```

### 📂 Copied to Repository:

```
training/results/
├── best.pt
├── last.pt
├── confusion_matrix.png
├── precision_curve.png
├── recall_curve.png
├── F1_curve.png
├── P_curve.png
├── R_curve.png
├── results.csv
└── weights/
```

### Model updated:
```
model/
├── best.pt      ← Updated with latest trained weights
└── ...
```

---

## Step 5: Expected Output During Training

You'll see output like:

```
🔵 TouchVision Backend Initializing...
✅ YOLOv8 detector loaded

🚀 Starting YOLO Training...
Epoch 1/100: [████████░░] 80% - 23ms/img, 0.45 loss
Epoch 2/100: [████████░░] 80% - 22ms/img, 0.42 loss
Epoch 3/100: [████████░░] 80% - 21ms/img, 0.39 loss
...
Epoch 100/100: [██████████] 100% - 20ms/img, 0.15 loss

Training completed!
✓ Results saved to: runs/detect/braille_dot_detector/
✓ Copied best.pt to model/
✓ Training metrics:
  - mAP@0.5: 0.87
  - Precision: 0.85
  - Recall: 0.83
```

---

## Step 6: Verify Everything Works

### Check Results:

```bash
# List generated files
dir training/results\

# View confusion matrix
# Open in image viewer: training/results/confusion_matrix.png

# Check metrics CSV
type training\results\results.csv
```

### Update README with Real Metrics:

The README already has placeholder metrics. After training, update with your actual results:

```markdown
## Model Performance (Actual Results)

| Metric | Value |
|---|---|
| mAP@0.5 | ~0.87 |
| Precision | ~0.85 |
| Recall | ~0.83 |
| Training Epochs | 100 |
| Inference Speed (CPU) | ~45ms/frame |
| Inference Speed (GPU) | ~12ms/frame |
```

---

## Step 7: Commit to GitHub (For Submission)

```bash
# Add all new files
git add .

# Commit with message
git commit -m "Add training metrics, confusion matrix, and model performance data"

# Push to GitHub
git push origin main
```

---

## Troubleshooting

### ❌ "Dataset not found" Error

**Solution:**
- Verify `dataset/images/train/` has `.jpg`/`.png` files
- Verify `dataset/labels/train/` has `.txt` files
- Check `dataset/data.yaml` paths are correct

### ❌ "CUDA out of memory"

**Solution:** Reduce batch size:
```bash
yolo detect train ... batch=8  # instead of 16
```

Or use CPU (slower but works):
```bash
yolo detect train ... device=cpu
```

### ❌ "No training images found"

**Solution:** Check YOLO label format. Each image must have corresponding `.txt` file with format:
```
<class_id> <x_center> <y_center> <width> <height>
0 0.5 0.5 0.3 0.4
```

### ❌ Training too slow

**Solution:**
- Use smaller model: `yolov8n.pt` (Nano - fastest)
- Use GPU: `device=0` instead of `device=cpu`
- Use smaller images: `imgsz=416` instead of `imgsz=640`

---

## Timeline Estimates

| Task | Time | Notes |
|---|---|---|
| Download dataset | 5-15 min | Depends on size |
| Organize files | 5 min | Copy to correct folders |
| Run training (GPU) | 30-60 min | 100 epochs on GPU |
| Run training (CPU) | 3-5 hours | 100 epochs on CPU |
| Generate metrics | Auto | Done during training |
| Commit to GitHub | 2 min | Push results |
| **Total** | **45 min - 6 hours** | Depends on GPU availability |

---

## After Training is Complete

Your repository will have:

✅ **Best trained model** (`model/best.pt`)  
✅ **Confusion matrix** (visualization)  
✅ **Performance metrics** (CSV with epoch data)  
✅ **Precision/Recall curves** (PNG plots)  
✅ **Complete project structure** (ready for submission)  

🎉 **Ready for Hackathon 2026 Submission!**

---

## Questions?

If you run into issues:
1. Check that dataset structure matches exactly
2. Verify `data.yaml` file paths
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Try with smaller batch size or shorter epochs first
