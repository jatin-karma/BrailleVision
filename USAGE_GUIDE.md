# 🎯 TouchVision Usage Guide

Complete guide on how to use the TouchVision repository, model, and API.

---

## Table of Contents

1. [Quick Start (5 min)](#quick-start)
2. [Web Interface Usage](#web-interface-usage)
3. [API Usage](#api-usage)
4. [Using the Model Directly](#using-the-model-directly)
5. [Command Line Usage](#command-line-usage)
6. [Python Integration](#python-integration)
7. [Advanced Usage](#advanced-usage)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### For Non-Technical Users (Web Interface)

**Step 1: Clone the Repository**
```bash
git clone https://github.com/jatin-karma/TouchVision.git
cd TouchVision
```

**Step 2: Install Dependencies**
```bash
# Python dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

**Step 3: Start Backend (Terminal 1)**
```bash
python -m uvicorn backend.app:app --reload
```
Expected output:
```
✅ TouchVision Backend Initializing...
✅ YOLOv8 detector loaded
✅ TTS engine initialized
Uvicorn running on http://0.0.0.0:8000
```

**Step 4: Start Frontend (Terminal 2)**
```bash
cd frontend
npm run dev
```
Expected output:
```
VITE v5.x.x ready in xxx ms
➜  Local:   http://localhost:5173
```

**Step 5: Open Website**
Open browser and go to: **http://localhost:5173**

**Step 6: Upload Braille Image**
1. Click "Upload" button
2. Select a JPG/PNG image of Braille dots
3. Click "Process"
4. See detected text and confidence
5. Click "Speak" to hear the result

---

## Web Interface Usage

### Features Available in Web App

**Image Upload**
- Click upload button
- Supports: JPG, PNG, BMP formats
- Max size: Limited by browser
- Recommended: 640x480 or larger

**Live Detection**
- Shows bounding boxes around detected dots
- Color-coded boxes with confidence scores
- Visual feedback on detection quality

**Decoded Text Display**
- Shows recognized Braille characters
- Displays confidence percentage
- Shows number of cells found

**Text-to-Speech (TTS)**
- Click "Speak" button to hear result
- Automatically pronounces detected text
- Useful for verification

**Multiple Uploads**
- Process as many images as needed
- Results shown one at a time
- Download annotated images

---

## API Usage

### Base URL
```
http://localhost:8000
```

### Authentication
No authentication required for local use.

### Endpoints

#### 1. Health Check
**Endpoint:** `GET /`

**Purpose:** Check if API is running

**Example:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "running",
  "app": "TouchVision",
  "version": "1.0.0",
  "detector_loaded": true,
  "tts_loaded": true
}
```

---

#### 2. Predict (Main Endpoint)
**Endpoint:** `POST /predict`

**Purpose:** Detect and decode Braille from image

**Parameters:**
- `file` (required): Image file (JPG, PNG)

**Request Example (cURL):**
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@braille_image.jpg"
```

**Request Example (Python):**
```python
import requests

with open("braille_image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/predict",
        files={"file": f}
    )

result = response.json()
print(result)
```

**Response:**
```json
{
  "text": "TouchVision",
  "confidence": 0.87,
  "dots_detected": 18,
  "cells_found": 6,
  "annotated_image": "data:image/jpeg;base64,..."
}
```

**Response Fields:**
- `text`: Detected Braille as text
- `confidence`: Average confidence (0-1)
- `dots_detected`: Estimated dot count
- `cells_found`: Number of Braille cells detected
- `annotated_image`: Base64-encoded annotated image

---

#### 3. Text-to-Speech
**Endpoint:** `POST /speak`

**Purpose:** Convert text to speech

**Parameters:**
- `text` (required): Text to speak

**Request Example (cURL):**
```bash
curl -X POST http://localhost:8000/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello World"}'
```

**Request Example (Python):**
```python
import requests

response = requests.post(
    "http://localhost:8000/speak",
    json={"text": "TouchVision"}
)

print(response.json())
```

**Response:**
```json
{
  "status": "spoken",
  "text": "Hello World"
}
```

---

#### 4. Raw Detection (Debug)
**Endpoint:** `POST /detect-raw`

**Purpose:** Get raw detection results without decoding

**Parameters:**
- `file` (required): Image file

**Response:**
```json
{
  "boxes": [[x1, y1, x2, y2], ...],
  "confidences": [0.95, 0.92, ...],
  "count": 6
}
```

---

#### 5. API Information
**Endpoint:** `GET /info`

**Purpose:** Get system information

**Example:**
```bash
curl http://localhost:8000/info
```

**Response:**
```json
{
  "app": "TouchVision",
  "version": "1.0.0",
  "endpoints": {
    "GET /": "Health check",
    "POST /predict": "Predict Braille from image",
    "POST /speak": "Convert text to speech",
    "POST /detect-raw": "Raw detection (debugging)",
    "GET /info": "This endpoint"
  },
  "model_loaded": true,
  "tts_available": true
}
```

---

## Using the Model Directly

### Python Integration

**Simple Usage:**
```python
from backend.core.detector import BrailleDetector
import cv2

# Load detector
detector = BrailleDetector()

# Load image
image = cv2.imread("braille_image.jpg")

# Detect
boxes, confidences, labels, annotated = detector.detect_with_annotated(image)

# Results
for box, label, conf in zip(boxes, labels, confidences):
    print(f"Detected: {label} (Confidence: {conf:.2f})")
    print(f"Location: {box}")
```

**Full Pipeline:**
```python
from backend.core.preprocessor import preprocess
from backend.core.detector import BrailleDetector
from backend.core.cell_grouper import group_into_cells
from backend.core.decoder import decode_cells
import cv2

# 1. Load image
image = cv2.imread("braille_image.jpg")

# 2. Preprocess
preprocessed = preprocess(image)

# 3. Detect dots
detector = BrailleDetector()
boxes, confs = detector.detect(preprocessed)

# 4. Group into cells
cells = group_into_cells(boxes)

# 5. Decode
text = decode_cells(cells)

print(f"Decoded Text: {text}")
```

**With TTS:**
```python
from backend.core.tts_engine import TTSEngine

# After decoding...
tts = TTSEngine()
tts.speak(text)  # Speak the detected text
```

### Using YOLOv8 Directly

**Without the custom pipeline:**
```python
from ultralytics import YOLO
import cv2

# Load model
model = YOLO("model/best.pt")

# Run inference
image = cv2.imread("braille_image.jpg")
results = model.predict(image, conf=0.35)

# Process results
for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        confidence = box.conf[0]
        print(f"Confidence: {confidence:.2f}")
        print(f"Box: ({x1}, {y1}) to ({x2}, {y2})")

# Save annotated image
annotated = results[0].plot()
cv2.imwrite("output.jpg", annotated)
```

---

## Command Line Usage

### Using Inference Script

**Single Image:**
```bash
python inference/inference.py --source braille.jpg --weights model/best.pt
```

**Webcam:**
```bash
python inference/inference.py --source 0 --weights model/best.pt
```

**Folder of Images:**
```bash
python inference/inference.py --source images/ --weights model/best.pt
```

**With Custom Settings:**
```bash
python inference/inference.py \
  --source braille.jpg \
  --weights model/best.pt \
  --conf 0.4 \
  --imgsz 640
```

---

## Python Integration

### Using in Your Own Project

**Installation:**
```bash
# Copy to your project
cp -r TouchVision/backend your_project/

# Install dependencies
pip install -r your_project/backend/requirements.txt
```

**Import and Use:**
```python
import sys
sys.path.insert(0, 'path/to/TouchVision')

from backend.core.detector import BrailleDetector
from backend.core.cell_grouper import group_into_cells
from backend.core.decoder import decode_cells

# Use as needed
detector = BrailleDetector()
# ... rest of code
```

### As a Module

```python
# Create your_braille_module.py
from backend.core.detector import BrailleDetector

class BrailleReader:
    def __init__(self):
        self.detector = BrailleDetector()
    
    def read(self, image_path):
        # Your implementation
        pass

# Use it
reader = BrailleReader()
text = reader.read("image.jpg")
```

---

## Advanced Usage

### Batch Processing

**Process Multiple Images:**
```python
import os
import requests
from pathlib import Path

API_URL = "http://localhost:8000/predict"
input_dir = "sample_images"
output_dir = "results"

Path(output_dir).mkdir(exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(('.jpg', '.png')):
        filepath = os.path.join(input_dir, filename)
        
        with open(filepath, 'rb') as f:
            response = requests.post(API_URL, files={'file': f})
        
        result = response.json()
        
        # Save result
        with open(f"{output_dir}/{filename}.txt", 'w') as f:
            f.write(f"Text: {result['text']}\n")
            f.write(f"Confidence: {result['confidence']}\n")
        
        print(f"{filename}: {result['text']}")
```

### Real-time Processing

```python
import cv2
from backend.core.detector import BrailleDetector

detector = BrailleDetector()
cap = cv2.VideoCapture(0)  # Webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect
    boxes, confs, labels, annotated = detector.detect_with_annotated(frame)
    
    # Show
    cv2.imshow('TouchVision', annotated)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Custom Confidence Threshold

```python
from backend.core.detector import BrailleDetector

detector = BrailleDetector()

# Default threshold: 0.35
# Custom threshold: 0.6
image = cv2.imread("braille.jpg")
boxes, confs = detector.detect(image, conf=0.6)

# Only high-confidence detections
high_conf = [(b, c) for b, c in zip(boxes, confs) if c > 0.8]
```

### Save Annotated Images

```python
import cv2
from backend.core.detector import BrailleDetector

detector = BrailleDetector()
image = cv2.imread("braille.jpg")

boxes, confs, labels, annotated = detector.detect_with_annotated(image)

# Save
cv2.imwrite("output_annotated.jpg", annotated)
```

---

## Troubleshooting

### Issue: Model not loading

**Error Message:**
```
FileNotFoundError: Model weights not found at model/best.pt
```

**Solutions:**
1. Check if `model/best.pt` exists
2. Download from: [Google Drive Link or Model Storage]
3. Place in `TouchVision/model/` directory

---

### Issue: Import errors

**Error Message:**
```
ModuleNotFoundError: No module named 'ultralytics'
```

**Solution:**
```bash
pip install -r requirements.txt
```

---

### Issue: CORS error in frontend

**Error Message:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Cause:** Backend not running

**Solution:**
```bash
python -m uvicorn backend.app:app --reload
```

---

### Issue: Port already in use

**Error Message:**
```
ERROR: Address already in use
```

**Solution 1: Kill existing process**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

**Solution 2: Use different port**
```bash
python -m uvicorn backend.app:app --port 8001
```

---

### Issue: Low detection accuracy

**Possible Causes:**
- Image quality too low
- Image lighting poor
- Braille too small
- Model needs retraining on your data

**Solutions:**
1. Use high-quality images (640x480 or larger)
2. Improve lighting
3. Ensure Braille is clearly visible
4. Retrain model with your data

---

### Issue: Slow inference

**Possible Causes:**
- Using CPU (no GPU)
- Large image size
- Model too large

**Solutions:**
1. Use GPU if available
2. Resize images to 640x640
3. Use YOLOv8 Nano (current default)

---

## Performance Tips

### Optimize for Speed

**Use smaller images:**
```python
import cv2

image = cv2.imread("image.jpg")
image_small = cv2.resize(image, (640, 640))
```

**Use GPU (if available):**
```python
from ultralytics import YOLO

model = YOLO("model/best.pt")
results = model.predict(image, device=0)  # device=0 for GPU
```

**Batch processing:**
```python
from ultralytics import YOLO

model = YOLO("model/best.pt")
results = model.predict(images_list, batch=16)
```

### Optimize for Accuracy

**Use higher confidence threshold:**
```python
boxes, confs = detector.detect(image, conf=0.5)  # Filter low confidence
```

**Increase image size:**
```python
model.predict(image, imgsz=1280)  # Larger input
```

---

## Reference

**Model Details:**
- Type: YOLOv8 Nano
- Input: 640x640 pixels
- Classes: 1 (Braille dot)
- Weights: ~6 MB

**API Base:** `http://localhost:8000`

**Documentation:**
- README.md - Overview
- TRAINING_GUIDE.md - Training instructions
- PROJECT_LINKS.md - Important links

---

## Support

For issues or questions:
1. Check this guide's troubleshooting section
2. Review README.md
3. Check GitHub issues
4. Review code comments

---

**Last Updated:** 2026-05-31  
**Version:** 1.0.0
