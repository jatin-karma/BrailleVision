# 🔵 TouchVision — Real-Time Braille to English Converter

> **TouchVision Hackathon 2026 Submission**  
> Converts real physical handwritten/embossed Braille into English text and speech using live camera input.

---

## 📌 Project Overview

TouchVision is an assistive technology system that uses a camera to detect and decode real physical Braille dots from embossed or handwritten Braille surfaces and converts them into English text with optional text-to-speech (TTS) output.

**Core Pipeline:**
```
Camera Input → Preprocessing (OpenCV) → Dot Detection (YOLOv8) → Cell Grouping → Braille Decoding → English Text → TTS
```

### Accessibility Impact
- Sighted caregivers who cannot read Braille
- Digital archiving of physical Braille documents
- Real-time reading assistance for new Braille learners
- Institutions digitizing Braille educational materials

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Object Detection** | YOLOv8 (Ultralytics) |
| **Image Preprocessing** | OpenCV (cv2) |
| **Backend API** | FastAPI + Uvicorn |
| **Frontend** | React 18 + Vite |
| **Text-to-Speech** | pyttsx3 / gTTS |
| **Model Training** | YOLO on custom Braille dot dataset |
| **Model Format** | PyTorch (.pt) |
| **Dataset Annotation** | Roboflow |

---

## 📋 Setup Instructions

### Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18+ (for frontend)
- **Webcam** or USB camera (for real-time detection)
- **GPU** (optional: CUDA GPU for faster inference, CPU works fine)
- **Git** (for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/braillevision.git
cd braillevision
```

### 2. Backend Setup

Create a virtual environment and install dependencies:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

**Dependencies include:**
- `ultralytics` - YOLOv8 object detection
- `opencv-python` - Image processing
- `fastapi` & `uvicorn` - Web API framework
- `pyttsx3` & `gTTS` - Text-to-speech
- `numpy` & `Pillow` - Numerical & image operations

### 3. Frontend Setup

```bash
cd frontend
npm install
```

**Note:** Node modules are large (~300MB+) and will take a few minutes to download.

---

## ▶️ How to Run Locally

### Option A: With Frontend UI (Recommended)

**Terminal 1 - Start Backend API:**
```bash
# From project root
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

Output should show:
```
Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Start Frontend Dev Server:**
```bash
cd frontend
npm run dev
```

Output should show:
```
VITE v5.x.x ready in xxx ms
➜  Local:   http://localhost:5173
```

**Open your browser:** [http://localhost:5173](http://localhost:5173)

### Option B: API-Only (Command Line)

```bash
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

Then test with curl:
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@path/to/braille_image.jpg"
```

### Option C: CLI Inference (No Server)

For batch processing or testing without running the API:

```bash
python inference/inference.py --source path/to/image.jpg --weights model/best.pt
```

For live webcam detection:
```bash
python inference/inference.py --source 0 --weights model/best.pt
```

---

## 🔗 Sample Input/Output

### Sample Input Link
Provide a test image of Braille dots for inference:
- **Download Test Image:** [PASTE YOUR SAMPLE IMAGE LINK - See PROJECT_LINKS.md]
- **Google Drive Example:** `https://drive.google.com/file/d/FILE_ID/view`
- **Format:** JPG, PNG, or BMP
- **Size:** Recommended 640x480 or larger
- **Content:** Clear photo of embossed or handwritten Braille dots

### Sample Output Link
Example output with detected dots and decoded text:
- **Output Format:** JSON response with detected text and confidence scores
- **Example Output Path:** `outputs/` directory contains annotated images
- **Demo/Video Link:** [PASTE YOUR DEMO LINK - See PROJECT_LINKS.md]
- **Example:** Braille detection output showing visual annotations

### Example API Response
```json
{
  "text": "TouchVision",
  "confidence": 0.87,
  "dots_detected": 18,
  "cells_found": 6,
  "annotated_image": "data:image/jpeg;base64,..."
}
```

---

## 🏋️ Model Training & Google Colab

The YOLOv8 model was trained on custom Braille dot dataset. Here's how to replicate training on Google Colab:

### Step 1: Prepare Dataset (Google Drive)

1. **Upload your dataset to Google Drive:**
   - Create folder: `/TouchVision/dataset/` in Drive
   - Add annotated images and `data.yaml` configuration

2. **data.yaml format:**
   ```yaml
   path: /content/drive/MyDrive/TouchVision/dataset
   train: images/train
   val: images/val
   test: images/test
   nc: 1  # number of classes (dot detection = 1 class)
   names: ['dot']
   ```

### Step 2: Open Google Colab Notebook

1. Go to [Google Colab](https://colab.research.google.com)
2. Create a new notebook
3. Mount Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

### Step 3: Install YOLOv8

```python
# Install ultralytics
!pip install ultralytics opencv-python pillow pyyaml

# Import necessary libraries
from ultralytics import YOLO
import cv2
import os
```

### Step 4: Train the Model

```python
# Initialize YOLOv8 nano model
model = YOLO('yolov8n.pt')

# Start training
results = model.train(
    data='/content/drive/MyDrive/TouchVision/dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    patience=20,
    device=0,  # GPU device (0 = first GPU)
    name='braille_dot_detector',
    augment=True,
    momentum=0.937,
    weight_decay=0.0005
)

# Print results
print(f"mAP@0.5: {results.results_dict['metrics/mAP50']}")
print(f"Precision: {results.results_dict['metrics/precision']}")
print(f"Recall: {results.results_dict['metrics/recall']}")
```

### Step 5: Download Trained Weights

```python
# Download best weights to local machine
from google.colab import files

# Copy to Colab local storage
!cp runs/detect/braille_dot_detector/weights/best.pt ./best.pt

# Download to your computer
files.download('best.pt')
```

### Step 6: Use Trained Model Locally

1. Move downloaded `best.pt` to `model/` folder
2. Run inference:
   ```bash
   python -m uvicorn backend.app:app --reload
   ```

### Model Performance (Our Results)

| Metric | Value |
|---|---|
| mAP@0.5 | ~0.87 |
| Precision | ~0.85 |
| Recall | ~0.83 |
| Inference Speed (CPU) | ~45ms/frame |
| Inference Speed (GPU) | ~12ms/frame |

### Alternative: YOLOv8 Training Command (Local)

If training locally:
```bash
yolo detect train \
  data=dataset/data.yaml \
  model=yolov8n.pt \
  epochs=100 \
  imgsz=640 \
  batch=16 \
  name=braille_dot_detector \
  patience=20
```

---

## 🔍 Inference & Testing

### API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/
```

**Predict (Upload Image):**
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@braille_image.jpg"
```

**Text-to-Speech:**
```bash
curl -X POST http://localhost:8000/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello"}'
```

**Raw Detection (Debug):**
```bash
curl -X POST http://localhost:8000/detect-raw \
  -F "file=@braille_image.jpg"
```

**API Info:**
```bash
curl http://localhost:8000/info
```

### Batch Processing

Process multiple images:
```python
import requests
import os

API_URL = "http://localhost:8000/predict"
input_dir = "sample_inputs"

for filename in os.listdir(input_dir):
    if filename.endswith(('.jpg', '.png')):
        with open(os.path.join(input_dir, filename), 'rb') as f:
            response = requests.post(API_URL, files={'file': f})
            print(f"{filename}: {response.json()['text']}")
```

---

## 💻 Usage Guide: Using the Repository

### Quick Start (5 Minutes)

**1. Clone and Setup**
```bash
git clone https://github.com/jatin-karma/TouchVision.git
cd TouchVision
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

**2. Start Backend**
```bash
python -m uvicorn backend.app:app --reload
```
*API will be available at: http://localhost:8000*

**3. Start Frontend (New Terminal)**
```bash
cd frontend
npm run dev
```
*Web app will be available at: http://localhost:5173*

**4. Open Browser**
Navigate to: http://localhost:5173

**5. Upload Braille Image**
- Click upload button
- Select a Braille image
- See detected Braille and decoded text
- Click "Speak" to hear the result

### Using the Model Directly

**Python Code Example:**
```python
from backend.core.detector import BrailleDetector
from backend.core.preprocessor import preprocess
from backend.core.cell_grouper import group_into_cells
from backend.core.decoder import decode_cells
import cv2

# Load image
image = cv2.imread("path/to/braille.jpg")

# Initialize detector
detector = BrailleDetector()

# Preprocess
preprocessed = preprocess(image)

# Detect dots
boxes, confidences = detector.detect(preprocessed)

# Group and decode
cells = group_into_cells(boxes)
text = decode_cells(cells)

print(f"Detected: {text}")
```

**Using YOLOv8 Directly:**
```python
from ultralytics import YOLO
import cv2

# Load model
model = YOLO("model/best.pt")

# Run inference
image = cv2.imread("braille_image.jpg")
results = model.predict(image)

# Get detections
for result in results:
    print(f"Boxes: {result.boxes}")
    print(f"Confidence: {result.boxes.conf}")
```

### API Usage Examples

**Python with Requests:**
```python
import requests

# Upload and predict
with open("braille_image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/predict",
        files={"file": f}
    )
    
result = response.json()
print(f"Text: {result['text']}")
print(f"Confidence: {result['confidence']}")
print(f"Cells Found: {result['cells_found']}")
```

**JavaScript/Frontend:**
```javascript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log("Detected text:", result.text);
console.log("Confidence:", result.confidence);
```

**cURL (Command Line):**
```bash
# Predict from image
curl -X POST http://localhost:8000/predict \
  -F "file=@braille_image.jpg" | jq

# Get API info
curl http://localhost:8000/info | jq

# Speak detected text
curl -X POST http://localhost:8000/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello World"}'
```

### Model Information

**Model Type:** YOLOv8 Nano (Lightweight)
**Input Size:** 640x640 pixels
**Classes:** 1 (Braille dot detection)
**Format:** PyTorch (.pt)
**Size:** ~6 MB
**Speed:** ~45ms/frame (CPU), ~12ms/frame (GPU)

**Model Location:**
- `model/best.pt` - Use this for inference
- Trained on custom Braille dot dataset
- See `model/model_info.md` for details

### Directory Structure Quick Reference

```
TouchVision/
├── backend/          ← FastAPI server (start here)
│   ├── app.py       ← Main application
│   ├── config.py    ← Configuration
│   └── core/        ← Core modules (detection, decoding, TTS)
│
├── frontend/        ← React web interface
│   └── src/         ← React components
│
├── model/           ← Trained YOLOv8 model
│   └── best.pt      ← Use this for inference
│
├── inference/       ← Inference scripts
│   ├── inference.py
│   └── predict.py
│
├── training/        ← Training scripts
│   ├── train.py
│   └── BV.py
│
├── dataset/         ← Dataset config
│   └── data.yaml
│
├── README.md        ← This file
├── TRAINING_GUIDE.md    ← Training instructions
└── PROJECT_LINKS.md     ← Important links
```

### Common Tasks

**Task: Run inference on single image**
```bash
python inference/inference.py --source braille.jpg --weights model/best.pt
```

**Task: Test with webcam**
```bash
python inference/inference.py --source 0 --weights model/best.pt
```

**Task: Process batch of images**
```bash
python inference/inference.py --source images/ --weights model/best.pt
```

**Task: Get API response in JSON**
```bash
curl -X POST http://localhost:8000/predict -F "file=@image.jpg" | python -m json.tool
```

**Task: Custom text-to-speech**
```bash
curl -X POST http://localhost:8000/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"TouchVision"}'
```

### Troubleshooting Usage Issues

**Issue: Model not loading**
```
Error: Model weights not found at model/best.pt
```
Solution: Ensure `model/best.pt` exists. Download from model storage.

**Issue: CORS error in frontend**
```
Error: Access to XMLHttpRequest blocked by CORS
```
Solution: Backend is running. Check `backend/config.py` CORS settings.

**Issue: Port already in use**
```
ERROR: Address already in use
```
Solution: Change port number:
```bash
python -m uvicorn backend.app:app --port 8001
```

**Issue: No camera detected**
```
Error: Camera not found
```
Solution: Check camera permissions or use image files instead.

---

## 📁 Project Structure

```
braillevision/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── setup_instructions.md              # Quick setup reference
├── ai_tools_disclosure.md             # AI tools used
│
├── frontend/                          # React + Vite web interface
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── src/
│   │   ├── App.jsx                   # Main component
│   │   ├── App.css
│   │   ├── main.jsx
│   │   ├── components/
│   │   │   ├── CameraFeed.jsx        # Live camera input
│   │   │   ├── ControlPanel.jsx      # UI controls
│   │   │   ├── ResultDisplay.jsx     # Shows detected text
│   │   │   ├── ResultSection.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── SpeakButton.jsx       # TTS button
│   │   └── assets/
│   │       ├── logo.png
│   │       └── brand.jpg
│   ├── dist/                         # Build output (generated)
│   └── node_modules/                 # Dependencies (generated)
│
├── backend/                          # FastAPI backend
│   ├── app.py                        # Main API server
│   ├── config.py                     # Configuration
│   └── core/
│       ├── __init__.py
│       ├── preprocessor.py           # Image preprocessing (CLAHE, blur, threshold)
│       ├── detector.py               # YOLOv8 dot detection
│       ├── cell_grouper.py           # Groups dots into cells
│       ├── decoder.py                # Braille to English mapping
│       └── tts_engine.py             # Text-to-speech
│
├── model/                            # Trained model weights
│   ├── best.pt                       # Best trained weights (6MB)
│   ├── model_info.md                 # Model details
│   └── DOWNLOAD_WEIGHTS.txt
│
├── training/                         # Training scripts
│   ├── train.py                      # Training entry point
│   ├── BV.py                         # Custom training logic
│   ├── yolo_train_command.txt        # Reference training command
│   └── results/                      # Training outputs (metrics, plots)
│
├── dataset/                          # Training dataset
│   ├── data.yaml                     # Dataset configuration (paths, classes)
│   ├── dataset_info.md               # Dataset documentation
│   └── [sample_images, labels]
│
├── inference/                        # Inference/testing scripts
│   ├── inference.py                  # CLI inference tool
│   ├── predict.py                    # Prediction utilities
│   └── test_inference.py             # Unit tests
│
├── demo/                             # Demo materials
│   ├── demo_video_link.txt
│   └── screenshots/
│
├── uploads/                          # User uploaded images (runtime)
├── outputs/                          # Inference results (runtime)
└── runs/                             # YOLO training runs (generated)
```

---



## 🛠️ Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
# Windows:
netstat -ano | findstr :8000
# macOS/Linux:
lsof -i :8000

# Kill the process and try again
```

### Model weights not found
```
Error: Model weights not found at model/best.pt
```
**Solution:** Download `best.pt` from model storage and place in `model/` folder.

### Frontend won't connect to backend
```bash
# Ensure CORS is configured correctly (check backend/config.py)
# Default allowed origins:
# - http://localhost:5173
# - http://127.0.0.1:5173
```



---

## 📊 Performance Benchmarks

| Component | Metric | Value |
|---|---|---|
| **Detection** | mAP@0.5 | 0.87 |
| **Detection** | Precision | 0.85 |
| **Detection** | Recall | 0.83 |
| **Inference** | Speed (CPU) | ~45ms/frame |
| **Inference** | Speed (GPU) | ~12ms/frame |
| **API** | Response Time | <100ms (with image encode) |
| **Frontend** | Build Size | ~150KB (gzipped) |

---

## 📚 Documentation Links

- **Setup Guide:** See `setup_instructions.md`
- **AI Tools Disclosure:** See `ai_tools_disclosure.md`
- **Dataset Info:** See `dataset/dataset_info.md`
- **Model Details:** See `model/model_info.md`
- **Project Links:** See `PROJECT_LINKS.md` ⭐ (Update with your Google Drive links)

---


## 🙏 Acknowledgments

- **YOLOv8** - Ultralytics for powerful object detection
- **Roboflow** - Dataset annotation and augmentation platform
- **Google Colab** - Free GPU resources for model training
- **FastAPI** - Modern async web framework
- **React** - Frontend UI framework

