# TouchVision — Setup Instructions

## Prerequisites

Ensure you have the following installed:

- **Python 3.10+** (verify with `python --version`)
- **Node.js 18+** (verify with `node --version`)
- **npm** (comes with Node.js)
- **Git** (for cloning the repository)
- **Webcam** or USB camera (for real-time inference)
- **CUDA 11.8+** (optional, for GPU acceleration)

---

## Step-by-Step Setup

### 1. Navigate to Project Directory

```bash
cd d:\TouchVision
```

### 2. Create a Python Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install. This may take 5-10 minutes.

### 4. Download YOLOv8 Model Weights

Download `best.pt` from the link provided in `model/model_info.md` and place it in the `model/` folder:

```
model/best.pt  ← Place the file here
```

Alternatively, the system will attempt to download it automatically on first run.

### 5. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 6. Verify the Setup

Test backend:
```bash
cd backend
python -c "from core.detector import BrailleDetector; print('✅ Backend setup OK')"
```

Test frontend:
```bash
cd frontend
npm list
```

---

## Running the Application

### Start Backend Server

```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Started server process [XXXX]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Start Frontend (in a new terminal)

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v4.X.X  ready in XXX ms

➜  Local:   http://localhost:5173/
```

### Open in Browser

Navigate to: **http://localhost:5173**

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'ultralytics'"

**Solution:** Ensure requirements.txt was installed correctly:
```bash
pip install -r requirements.txt
```

### Issue: "Model weights not found at: model/best.pt"

**Solution:** Download the model weights from the provided Google Drive/Hugging Face link and place in `model/best.pt`.

### Issue: Port 8000 already in use

**Solution:** Use a different port:
```bash
uvicorn app:app --port 8001
```

### Issue: Port 5173 already in use

**Solution:** Vite will automatically try the next available port.

### Issue: Camera not detected

**Solution:**
- Ensure camera is plugged in and recognized by OS
- Check browser camera permissions (usually in address bar)
- Try testing with a sample image instead of live camera

---

## Running Inference from CLI

Test inference on a sample image:

```bash
python inference/inference.py --source path/to/braille_image.jpg --weights model/best.pt
```

For live camera:
```bash
python inference/inference.py --source 0 --weights model/best.pt --live
```

---

## Development Tips

- **Backend hot-reload:** Use `--reload` with uvicorn (already enabled above)
- **Frontend hot-reload:** Vite automatically reloads on file changes
- **Debug mode:** Add `--reload` to uvicorn for debugging
- **CORS issues:** If frontend can't reach backend, check CORS config in `backend/config.py`

---

## Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
MODEL_PATH=model/best.pt
CONF_THRESHOLD=0.35
BACKEND_PORT=8000
FRONTEND_PORT=5173
```

---

## Hardware Acceleration (GPU)

To enable CUDA GPU acceleration:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install ultralytics[gpu]
```

---

## Support

For issues or questions, contact: [your-email@example.com]

For model weights access: [Google Drive / Hugging Face link]
