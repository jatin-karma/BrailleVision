"""
Batch prediction helper for TouchVision.
Processes multiple images and generates results.
"""

import os
import cv2
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.preprocessor import preprocess
from backend.core.detector import BrailleDetector
from backend.core.cell_grouper import group_into_cells
from backend.core.decoder import decode_cells


def predict_batch(image_dir: str, weights: str = "model/best.pt", output_file: str = None):
    """
    Process all images in a directory.
    
    Args:
        image_dir: Directory containing images
        weights: Path to model weights
        output_file: Optional CSV file to save results
    """
    
    detector = BrailleDetector(weights)
    results = []
    
    image_files = list(Path(image_dir).glob("*.jpg")) + list(Path(image_dir).glob("*.png"))
    
    print(f"Processing {len(image_files)} images...")
    
    for image_path in image_files:
        image = cv2.imread(str(image_path))
        if image is None:
            continue
        
        # Process
        processed = preprocess(image)
        boxes, confs = detector.detect(processed)
        cells = group_into_cells(boxes)
        text = decode_cells(cells)
        
        result = {
            'filename': image_path.name,
            'decoded_text': text,
            'dots_detected': len(boxes),
            'cells_found': len(cells),
            'avg_confidence': float(np.mean(confs)) if confs else 0.0,
        }
        results.append(result)
        
        print(f"  ✓ {image_path.name}: {text}")
    
    # Save results if requested
    if output_file:
        import csv
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\n✅ Results saved to {output_file}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", type=str, required=True, help="Directory with images")
    parser.add_argument("--weights", type=str, default="model/best.pt", help="Model weights")
    parser.add_argument("--output", type=str, default=None, help="Output CSV file")
    
    args = parser.parse_args()
    predict_batch(args.image_dir, args.weights, args.output)
