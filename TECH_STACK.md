# 🛠️ TouchVision — Tech Stack

## Backend

**Framework:** FastAPI (Python)
- Async web framework for building APIs
- High performance, easy to use, auto-generated API documentation

**Object Detection:** YOLOv8 (Ultralytics)
- Lightweight nano model for real-time Braille dot detection
- Pre-trained on COCO, fine-tuned on custom Braille dataset
- ~6MB model size, 45ms/frame CPU, 12ms/frame GPU

**Image Processing:** OpenCV (cv2)
- CLAHE enhancement for low-contrast images
- Gaussian blur and adaptive thresholding
- Morphological operations for preprocessing
- Base64 encoding for API responses

**Numerical Computing:** NumPy
- Array operations for detection box manipulation
- Confidence score aggregation and statistics

**Core Python Libraries:**
- `python-multipart` - File upload handling
- `pydantic` - Data validation
- `uvicorn` - ASGI server

## Frontend

**Framework:** React 18
- Component-based UI architecture
- 8 reusable components (CameraFeed, ResultDisplay, SpeakButton, etc.)
- State management with React hooks

**Build Tool:** Vite
- Fast development server
- Optimized production builds
- ~150KB gzipped bundle size

**Styling:** CSS3
- Responsive design
- Mobile-friendly interface

## Machine Learning

**Training:** YOLOv8 (Ultralytics)
- Command-line training interface
- Automatic augmentation pipeline
- Real-time metric tracking

**Dataset Management:** Roboflow
- Annotation platform for bounding boxes
- Automated augmentation (rotation, flip, brightness jitter)
- YOLO format export

**Training Environment:** Google Colab
- Free GPU resources (T4/K80)
- Pre-configured ML environment
- Easy dataset integration via Google Drive

## Infrastructure

**Version Control:** Git + GitHub
- Clean commit history
- Collaborative development
- Public repository for transparency

**Package Management:**
- Python: pip + requirements.txt
- Node.js: npm + package.json

**Text-to-Speech:** pyttsx3 + gTTS
- Cross-platform TTS support
- Offline capability (pyttsx3)
- Cloud option (gTTS)

## Performance

- CPU Inference: ~45ms/frame
- GPU Inference: ~12ms/frame
- Model Accuracy: mAP@0.5 = 0.87
- Frontend Load Time: <1s
- API Response: <100ms

**Total Dependencies:** 15 core packages
**Code Size:** ~50 source files
**Documentation:** 1400+ lines
