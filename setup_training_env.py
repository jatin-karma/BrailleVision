#!/usr/bin/env python3
"""
Setup training environment and run YOLO training to generate metrics.
This script will:
1. Verify dataset structure
2. Run YOLO training
3. Generate confusion matrix, metrics, and curves
4. Copy results to training/results/ directory
"""

import os
import shutil
from pathlib import Path
import subprocess
import sys

def check_dataset():
    """Check if dataset exists and has images."""
    dataset_path = Path("dataset")

    print("📁 Checking dataset structure...")

    # Check for images
    train_images = list(dataset_path.glob("images/train/*.jpg")) + \
                   list(dataset_path.glob("images/train/*.png"))
    val_images = list(dataset_path.glob("images/val/*.jpg")) + \
                 list(dataset_path.glob("images/val/*.png"))

    print(f"  Training images: {len(train_images)}")
    print(f"  Validation images: {len(val_images)}")

    return len(train_images) > 0 and len(val_images) > 0

def setup_directories():
    """Create necessary directories."""
    dirs = [
        "dataset/images/train",
        "dataset/images/val",
        "dataset/images/test",
        "dataset/labels/train",
        "dataset/labels/val",
        "dataset/labels/test",
        "training/results",
    ]

    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

    print("✓ Directories created/verified")

def verify_data_yaml():
    """Verify data.yaml configuration."""
    data_yaml_path = Path("dataset/data.yaml")

    if not data_yaml_path.exists():
        print("✗ data.yaml not found")
        return False

    with open(data_yaml_path) as f:
        content = f.read()
        if "images/train" in content and "images/val" in content:
            print("✓ data.yaml is properly configured")
            return True
        else:
            print("✗ data.yaml paths are incorrect")
            return False

def run_training():
    """Run YOLO training."""
    print("\n🚀 Starting YOLO Training...")
    print("=" * 70)

    try:
        from ultralytics import YOLO
    except ImportError:
        print("✗ ultralytics not installed")
        print("Run: pip install ultralytics")
        return False

    try:
        # Load model
        model = YOLO('yolov8n.pt')

        # Train
        print("Training YOLOv8 model...")
        results = model.train(
            data='dataset/data.yaml',
            epochs=100,
            imgsz=640,
            batch=16,
            patience=20,
            device=0,  # GPU device
            name='braille_dot_detector',
            save=True,
            save_txt=True,
            plots=True,  # Generate plots
            augment=True,
        )

        print("=" * 70)
        print("✓ Training completed!")
        print(f"  Results saved to: runs/detect/braille_dot_detector/")

        # Copy best.pt to model folder
        src = Path("runs/detect/braille_dot_detector/weights/best.pt")
        dst = Path("model/best.pt")
        if src.exists():
            shutil.copy(src, dst)
            print(f"✓ Copied best.pt to model/")

        return True

    except Exception as e:
        print(f"✗ Training failed: {e}")
        return False

def copy_metrics_to_results():
    """Copy generated metrics to training/results."""
    print("\n📊 Organizing results...")

    results_dir = Path("runs/detect/braille_dot_detector")
    target_dir = Path("training/results")

    if not results_dir.exists():
        print("✗ Results directory not found")
        return False

    # Files to copy
    files_to_copy = [
        "confusion_matrix.png",
        "precision_curve.png",
        "recall_curve.png",
        "F1_curve.png",
        "P_curve.png",
        "R_curve.png",
        "results.csv",
    ]

    copied = 0
    for file in files_to_copy:
        src = results_dir / file
        dst = target_dir / file
        if src.exists():
            shutil.copy(src, dst)
            print(f"  ✓ {file}")
            copied += 1
        else:
            print(f"  - {file} (not found)")

    # Copy all weights
    weights_src = results_dir / "weights"
    weights_dst = target_dir / "weights"
    if weights_src.exists():
        if weights_dst.exists():
            shutil.rmtree(weights_dst)
        shutil.copytree(weights_src, weights_dst)
        print(f"  ✓ weights/")

    print(f"\n✓ Copied {copied} metric files to training/results/")
    return True

def print_instructions():
    """Print setup instructions."""
    print("\n" + "=" * 70)
    print("📋 SETUP INSTRUCTIONS")
    print("=" * 70)
    print("""
STEP 1: Prepare Dataset on Google Drive
────────────────────────────────────────
1. Go to your Google Drive where you trained on Colab
2. Find the TouchVision dataset folder
3. Download the following structure:

   dataset/
   ├── images/
   │   ├── train/  (training images)
   │   ├── val/    (validation images)
   │   └── test/   (test images)
   └── labels/
       ├── train/  (YOLO format labels)
       ├── val/    (YOLO format labels)
       └── test/   (YOLO format labels)

STEP 2: Place Dataset
──────────────────────
Place the downloaded dataset folder into:
  d:/TouchVision/dataset/

STEP 3: Run Training
─────────────────────
Option A (Automatic):
  $ python setup_training_env.py

Option B (Manual):
  $ yolo detect train \\
      data=dataset/data.yaml \\
      model=yolov8n.pt \\
      epochs=100 \\
      imgsz=640 \\
      batch=16 \\
      name=braille_dot_detector \\
      patience=20

STEP 4: Results
────────────────
After training, you'll have:
  ✓ runs/detect/braille_dot_detector/best.pt
  ✓ runs/detect/braille_dot_detector/confusion_matrix.png
  ✓ runs/detect/braille_dot_detector/precision_curve.png
  ✓ runs/detect/braille_dot_detector/recall_curve.png
  ✓ training/results/ (organized copies)

TROUBLESHOOTING:
─────────────────
If GPU not available:
  - Training will use CPU (slower, ~2-3 hours per epoch)
  - Use small batch size: batch=4 or batch=8

If out of memory:
  - Reduce batch size: batch=8
  - Reduce image size: imgsz=416

If dataset path errors:
  - Verify data.yaml paths are correct
  - Use absolute paths if needed
""")

def main():
    """Main setup function."""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║         YOLO Training Setup & Metrics Generation                 ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()

    # 1. Setup directories
    setup_directories()

    # 2. Verify data.yaml
    if not verify_data_yaml():
        print("\n✗ Please fix data.yaml first")
        return False

    # 3. Check dataset
    has_dataset = check_dataset()

    if not has_dataset:
        print("\n⚠️  Dataset images not found!")
        print_instructions()
        print("\nPlease download your dataset from Google Drive and place it in:")
        print("  d:/TouchVision/dataset/")
        return False

    # 4. Run training
    if not run_training():
        return False

    # 5. Copy metrics
    if not copy_metrics_to_results():
        print("⚠️  Some metrics could not be copied")

    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print("""
Generated files:
  ✓ training/results/ - All metric files
  ✓ model/best.pt - Updated model weights
  ✓ runs/detect/braille_dot_detector/ - Full training output

Next steps:
  1. Commit to git: git add . && git commit -m "Add training results"
  2. Push to GitHub: git push origin main
  3. Submit to Hackathon with complete metrics!
""")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Training cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
