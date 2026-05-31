"""
Inference script for TouchVision.
Performs end-to-end Braille detection and decoding on images or webcam feed.
"""

import argparse
import cv2
import numpy as np
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.preprocessor import preprocess
from backend.core.detector import BrailleDetector
from backend.core.cell_grouper import group_into_cells
from backend.core.decoder import decode_cells


def main(args):
    """Run inference on image, video, or webcam."""
    
    # Load detector
    try:
        detector = BrailleDetector(args.weights)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return
    
    # Process input
    if args.source == "0" or args.source == 0:
        # Webcam input
        print("📷 Opening webcam...")
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            processed = preprocess(frame)
            boxes, confs = detector.detect(processed)
            cells = group_into_cells(boxes)
            text = decode_cells(cells)
            
            # Draw on frame
            display_frame = frame.copy()
            for box in boxes:
                x1, y1, x2, y2 = [int(v) for v in box]
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Display text
            cv2.putText(display_frame, f"Braille: {text}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow("TouchVision Inference", display_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    else:
        # Image file input
        if not os.path.exists(args.source):
            print(f"❌ File not found: {args.source}")
            return
        
        image = cv2.imread(args.source)
        if image is None:
            print(f"❌ Could not read image: {args.source}")
            return
        
        # Process image
        print(f"Processing: {args.source}")
        processed = preprocess(image)
        boxes, confs = detector.detect(processed)
        cells = group_into_cells(boxes)
        text = decode_cells(cells)
        
        print(f"\n✅ Decoded Text: {text}")
        print(f"   Dots Detected: {len(boxes)}")
        print(f"   Cells Found: {len(cells)}")
        print(f"   Average Confidence: {np.mean(confs):.2f}" if confs else "   No detections")
        
        # Save output if requested
        if args.output:
            display_frame = image.copy()
            for box in boxes:
                x1, y1, x2, y2 = [int(v) for v in box]
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            cv2.putText(display_frame, f"Braille: {text}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imwrite(args.output, display_frame)
            print(f"   Saved to: {args.output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TouchVision Inference")
    parser.add_argument("--source", type=str, default="0", help="Image file or camera (0)")
    parser.add_argument("--weights", type=str, default="model/best.pt", help="Model weights path")
    parser.add_argument("--output", type=str, default=None, help="Output image path")
    
    args = parser.parse_args()
    main(args)
