from pathlib import Path
import sys

import pandas as pd

# Allow importing p2p_detector.py
sys.path.insert(0, str(Path(__file__).resolve().parent))

from p2p_detector import P2PAnomalyDetector


def main():
    detector = P2PAnomalyDetector()

    print("Model loaded successfully.")
    print("Number of features:", len(detector.features))
    print("Features:")
    for feature in detector.features:
        print(" -", feature)

    # Create a valid test input using neutral placeholder values.
    test_data = {
        feature: 0.0
        for feature in detector.features
    }

    result = detector.predict_one(test_data)

    print("\nTest prediction:")
    print(result)

    print("\nInference test PASSED.")


if __name__ == "__main__":
    main()