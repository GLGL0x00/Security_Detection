import sys

def main() -> int:
    try:
        import numpy as np
        import cv2
        import torch
        import ultralytics
        from ultralytics import YOLO
    except Exception as e:
        print(f"Import error: {e}")
        return 1

    print("versions:")
    print("  numpy:", np.__version__)
    print("  cv2:", cv2.__version__)
    print("  torch:", torch.__version__)
    print("  ultralytics:", ultralytics.__version__)

    # Try to initialize YOLO with a local weight file if present, otherwise skip
    try:
        yolo_path_candidates = [
            "bestface.pt",
            "best_lastTry.pt",
            "yolov8n.pt",
        ]
        for weight_path in yolo_path_candidates:
            try:
                model = YOLO(weight_path)
                print(f"YOLO init OK with: {weight_path}")
                break
            except Exception as inner:
                print(f"YOLO init failed with {weight_path}: {inner}")
        else:
            print("YOLO init skipped: no compatible weights loaded.")
    except Exception as e:
        print(f"YOLO check error: {e}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

