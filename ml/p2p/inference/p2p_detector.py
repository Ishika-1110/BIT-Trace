import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


class P2PAnomalyDetector:
    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = Path(__file__).resolve().parent.parent / "model"

        model_dir = Path(model_dir)

        self.model = joblib.load(
            model_dir / "isolation_forest.joblib"
        )

        self.scaler = joblib.load(
            model_dir / "scaler.joblib"
        )

        with open(model_dir / "feature_config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.features = self.config["features"]
        self.log1p_features = set(
            self.config.get("log1p_features", [])
        )

        thresholds = self.config.get("thresholds", {})

        self.high_threshold = thresholds.get(
            "high",
            thresholds.get("99th_percentile", None)
        )

        self.elevated_threshold = thresholds.get(
            "elevated",
            thresholds.get("95th_percentile", None)
        )

    def _prepare_features(self, data):
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            raise TypeError(
                "Input must be a dictionary or pandas DataFrame."
            )

        missing = [
            feature
            for feature in self.features
            if feature not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required features: {missing}"
            )

        df = df[self.features].copy()

        for feature in self.features:
            df[feature] = pd.to_numeric(
                df[feature],
                errors="coerce"
            )

        # Match training-time handling of undefined values.
        df = df.replace([np.inf, -np.inf], np.nan)

        for feature in self.features:
            if df[feature].isna().any():
                df[feature] = df[feature].fillna(0)

        # Apply the same log1p transformation used during training.
        for feature in self.log1p_features:
            if feature in df.columns:
                df[feature] = np.log1p(
                    np.clip(df[feature], a_min=0, a_max=None)
                )

        return df

    def predict(self, data):
        df = self._prepare_features(data)

        X_scaled = self.scaler.transform(df)

        # Training used:
        # anomaly_score = -IsolationForest.decision_function(X)
        anomaly_score = -self.model.decision_function(X_scaled)

        levels = []

        for score in anomaly_score:
            if (
                self.high_threshold is not None
                and score >= self.high_threshold
            ):
                levels.append("HIGH")
            elif (
                self.elevated_threshold is not None
                and score >= self.elevated_threshold
            ):
                levels.append("ELEVATED")
            else:
                levels.append("BASELINE")

        result = pd.DataFrame({
            "anomaly_score": anomaly_score,
            "candidate_level": levels
        })

        return result

    def predict_one(self, data):
        result = self.predict(data)
        return result.iloc[0].to_dict()