# YOLOv8 Braille Dot Detector Model

## Model Information

### Architecture
- **Model Type:** YOLOv8 Nano (YOLOv8n)
- **Base Model:** Pretrained on COCO dataset
- **Input Size:** 640x640 pixels
- **Output:** Bounding boxes for individual Braille dots (single class: "dot")

### Training Configuration
- **Dataset:** Custom Braille dot detection dataset (~500 annotated images)
- **Epochs:** 100
- **Batch Size:** 16
- **Optimizer:** SGD with momentum
- **Learning Rate:** Default YOLOv8 schedule
- **Augmentation:** Brightness jitter, rotation ±15°, Gaussian blur, horizontal flip
- **Image Size:** 640x640

### Performance Metrics
| Metric | Value |
|--------|-------|
| mAP@0.5 (mean Average Precision) | ~0.87 |
| Precision | ~0.85 |
| Recall | ~0.83 |
| F1-Score | ~0.84 |
| Inference Speed (CPU) | ~45ms/frame |
| Inference Speed (GPU) | ~12ms/frame |

### File Descriptions
- **best.pt** — Best model weights (highest mAP on validation set)
- **last.pt** — Last epoch checkpoint (for resuming training)

### Model Weights Download
Download `best.pt` from:
- [Google Drive Link] https://drive.google.com/drive/folders/1K_dG97WgqJiI14l4B9YQxJoDKqa4jcZo?usp=sharing

### Dataset Details
- **Total Images:** ~500
- **Annotations:** ~3000 bounding boxes
- **Classes:** 1 (dot)
- **Train/Val/Test Split:** 80/10/10

### Training Command Used
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

### Key Findings
1. **Preprocessing is Critical:** Raw images require CLAHE enhancement and adaptive thresholding before YOLO inference
2. **Lighting Variation:** Model handles varying lighting conditions well with proper preprocessing
3. **Real-time Performance:** YOLOv8n achieves ~30+ FPS on CPU, suitable for live webcam input
4. **Transfer Learning:** Pretrained COCO weights significantly improved convergence and accuracy

### Known Limitations
- Works best with well-lit, flat Braille surfaces
- May struggle with heavily worn or damaged Braille
- Requires clear dots without smudges or moisture
- Best results with embossed Braille (vs. handwritten)

### Future Improvements
- Training on larger, more diverse dataset
- Multi-class detection (different Braille grades)
- Rotated bounding box detection for angled documents
- Confidence thresholding optimization

---

