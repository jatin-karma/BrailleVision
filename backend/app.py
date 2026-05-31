"""
TouchVision FastAPI Backend.
Provides /predict and /speak endpoints for Braille detection and TTS.
"""

import base64
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CORS_ORIGINS, HOST, PORT, CONF_THRESHOLD
from core.preprocessor import preprocess
from core.detector import BrailleDetector
from core.cell_grouper import group_into_cells
from core.decoder import decode_cells, decode_with_confidence
from core.tts_engine import TTSEngine

# Initialize FastAPI app
app = FastAPI(
    title="TouchVision API",
    description="Real-time Braille to English converter",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
print("🔵 TouchVision Backend Initializing...")

try:
    detector = BrailleDetector()
    print("✅ YOLOv8 detector loaded")
except FileNotFoundError as e:
    print(f"❌ {e}")
    detector = None

try:
    tts = TTSEngine()
    print("✅ TTS engine initialized")
except Exception as e:
    print(f"⚠️  TTS unavailable: {e}")
    tts = None

print(f"✅ API running on {HOST}:{PORT}\n")


def _encode_image(image: np.ndarray) -> str:
    """Encode an OpenCV image as a base64 data URI."""
    success, buffer = cv2.imencode('.jpg', image)
    if not success:
        raise ValueError("Failed to encode annotated image")

    encoded = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{encoded}"


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "app": "TouchVision",
        "version": "1.0.0",
        "detector_loaded": detector is not None,
        "tts_loaded": tts is not None,
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict Braille text from uploaded image.
    
    Args:
        file: Image file (JPEG, PNG, etc.)
    
    Returns:
        JSON with decoded text and confidence
    """
    if detector is None:
        return JSONResponse(
            status_code=500,
            content={"error": "Detector not loaded. Model weights may be missing."}
        )
    
    try:
        # Read image from upload
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Could not decode image. Ensure it's a valid image file."}
            )
        
        # Detect dots and generate an annotated frame for display
        # We pass the original BGR frame so the annotated image remains in color.
        boxes, confs, labels, annotated = detector.detect_with_annotated(frame)
        
        text = ""
        if len(boxes) > 0:
            detected = []
            for box, label, conf in zip(boxes, labels, confs):
                cx = (box[0] + box[2]) / 2
                cy = (box[1] + box[3]) / 2
                detected.append({'cx': cx, 'cy': cy, 'label': label, 'conf': conf})
            
            # Sort by Y first, cluster into rows
            detected.sort(key=lambda d: d['cy'])
            rows = []
            current_row = []
            row_tol = 40  # Pixel tolerance for same row
            
            for d in detected:
                if not current_row:
                    current_row.append(d)
                elif abs(d['cy'] - current_row[0]['cy']) < row_tol:
                    current_row.append(d)
                else:
                    rows.append(current_row)
                    current_row = [d]
            if current_row:
                rows.append(current_row)
                
            # Sort each row by X and build text
            for row in rows:
                row.sort(key=lambda d: d['cx'])
                text += "".join(d['label'] for d in row) + " "
            
            text = text.strip()
            
        avg_confidence = float(np.mean(confs)) if len(confs) > 0 else 0.0
        
        return {
            "text": text,
            "confidence": avg_confidence,
            "dots_detected": len(boxes) * 3, # rough estimate since YOLO detects chars, not dots
            "cells_found": len(boxes),       # each box is a character cell
            "annotated_image": _encode_image(annotated),
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Prediction failed: {str(e)}"}
        )


@app.post("/speak")
async def speak(body: dict):
    """
    Convert text to speech.
    
    Args:
        body: JSON with 'text' field
    
    Returns:
        JSON with status
    """
    if tts is None:
        return JSONResponse(
            status_code=500,
            content={"error": "TTS engine not available"}
        )
    
    text = body.get("text", "").strip()
    
    if not text:
        return JSONResponse(
            status_code=400,
            content={"error": "No text provided"}
        )
    
    try:
        success = tts.speak(text)
        if success:
            return {"status": "spoken", "text": text}
        else:
            return JSONResponse(
                status_code=500,
                content={"error": "TTS failed to process text"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"TTS error: {str(e)}"}
        )


@app.post("/detect-raw")
async def detect_raw(file: UploadFile = File(...)):
    """
    Raw detection without decoding (for debugging).
    Returns detected boxes and confidence scores.
    """
    if detector is None:
        return JSONResponse(status_code=500, content={"error": "Detector not loaded"})
    
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return JSONResponse(status_code=400, content={"error": "Invalid image"})
        
        processed = preprocess(frame)
        boxes, confs = detector.detect(processed)
        
        return {
            "boxes": boxes,
            "confidences": confs,
            "count": len(boxes),
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/info")
async def info():
    """Get system information."""
    return {
        "app": "TouchVision",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "Health check",
            "POST /predict": "Predict Braille from image",
            "POST /speak": "Convert text to speech",
            "POST /detect-raw": "Raw detection (debugging)",
            "GET /info": "This endpoint",
        },
        "model_loaded": detector is not None,
        "tts_available": tts is not None,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
