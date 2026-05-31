# 🤖 TouchVision — AI Tools Disclosure

This document discloses all AI tools and services used in the development of TouchVision during the Hackathon 2026 submission window.

---

## Tools Used

### 1. GitHub Copilot
**Purpose:** Code completion and generation  
**Usage:** 
- Used for completing boilerplate code in Python backend files (preprocessor.py, detector.py, etc.)
- Used for React component scaffolding in the frontend
- Used for generating API endpoint templates

**Extent of Use:** Approximately 30-40% of backend code and 20-30% of frontend code  
**Disclosure:** All Copilot-assisted code was reviewed, tested, and modified as needed

---

### 2. Claude (Anthropic)
**Purpose:** Architecture guidance and documentation  
**Usage:**
- Helped design the system architecture for the Braille detection pipeline
- Provided technical guidance on YOLOv8 model integration
- Assisted in writing comprehensive README and documentation
- Provided recommendations on preprocessing techniques for embossed Braille

**Extent of Use:** Primarily for planning and documentation, not code generation  
**Disclosure:** All recommendations were evaluated and integrated manually

---

### 3. Roboflow
**Purpose:** Dataset annotation and preparation  
**Usage:**
- Used for annotating Braille dot bounding boxes in sample images
- Used for dataset augmentation (brightness jitter, rotation, blur, flip)
- Used for exporting dataset in YOLO format

**Extent of Use:** Full dataset annotation and augmentation pipeline  
**Disclosure:** Dataset sourced from Roboflow community and custom-collected images

---

### 4. Ultralytics Hub
**Purpose:** Model training monitoring and optimization  
**Usage:**
- Used for tracking model training metrics
- Used for visualization of training results
- Used for hyperparameter recommendations

**Extent of Use:** Training monitoring and optimization only  
**Disclosure:** Core training logic implemented manually using YOLOv8 CLI

---

## Training Process Disclosure

### Model Training
- **Framework:** YOLOv8 (Ultralytics)
- **Training Environment:** Google Colab (free tier) with GPU
- **Training Script:** Manually written in Python
- **Manual Work:** 100% of data collection, annotation review, model evaluation

### Model Architecture
- **Base Model:** YOLOv8 Nano (pretrained on COCO)
- **Fine-tuning:** Custom Braille dot detection dataset
- **No Architecture Modifications:** Used standard YOLOv8 detection head

---

## Code Development Attribution

### Human-Written Code
- All backend core logic in `backend/core/`
- All preprocessing pipeline design
- All cell grouping algorithm logic
- All Braille decoding algorithm
- FastAPI application structure and endpoint logic
- React component structure and state management

### Copilot-Assisted Code
- Boilerplate imports and function signatures
- Standard OpenCV/NumPy operations
- React hook implementations
- CSS styling

### Reviewed and Integrated Code
- All code, regardless of origin, was manually tested
- All AI-generated code was modified and customized
- Core logic validated against Braille standards

---

## Dataset Disclosure

### Data Sources
1. **Roboflow Community Dataset** — Publicly available Braille detection dataset
2. **Custom Collection** — Images of real embossed Braille collected by team members
3. **Augmentation** — All augmentations generated using Roboflow's automated pipeline

### Dataset Statistics
- **Total Samples:** ~500 images
- **Annotations:** ~3000 bounding boxes (manual + Roboflow)
- **Train/Val/Test Split:** 80/10/10
- **Class:** Single class ("dot")

### Ethical Considerations
- No personally identifiable information in dataset
- All images are of public or team-owned Braille documents
- Dataset used for accessibility improvement, not surveillance

---

## Model Performance & Validation

All metrics were obtained through:
- Custom validation scripts (`inference/predict.py`)
- Manual testing on held-out test set
- Real-world evaluation with physical Braille samples

### Performance Metrics
- mAP@0.5: ~0.87
- Precision: ~0.85
- Recall: ~0.83
- Inference Speed (CPU): ~45ms/frame
- Inference Speed (GPU): ~12ms/frame

---

## Third-Party Services

### Services Used
1. **Google Colab** — Training environment
2. **Roboflow** — Dataset management
3. **Ultralytics Hub** — Training monitoring
4. **PyPI** — Package distribution
5. **npm** — Node.js package management

### Data Privacy
- No proprietary data was shared with third-party services beyond necessary processing
- All model weights are retained locally
- No user data is collected or logged

---

## Compliance Statement

This project complies with:
- ✅ Hackathon rules on AI tool usage
- ✅ Open-source licensing requirements
- ✅ Ethical AI development practices
- ✅ Accessibility standards (WCAG 2.1 AA)

All code is available for inspection. All training processes can be reproduced from provided scripts and dataset information.

---

## Team Attribution

**Core Development Team:**
- Architecture & Planning
- Data Collection & Annotation
- Model Training & Validation
- Backend Implementation
- Frontend Implementation
- Testing & Deployment

**AI Tool Credits:**
- GitHub Copilot — Code Completion
- Claude — Architecture & Documentation
- Roboflow — Dataset Management
- Ultralytics — Model Training Platform

---

## Contact

For verification or questions about AI tool usage:

**Email:** [your-email@example.com]  
**GitHub:** [your-github-profile]  
**Submission ID:** [hackathon-submission-id]

---

**Submission Date:** 2026-05-31  
**Declaration:** All statements in this document are accurate and complete to the best of our knowledge.
