import numpy as np
from google.adk.tools import Tool
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest


class SequenceClusteringTool(Tool):
    name = "sequence_clustering"
    description = (
        "Clusters similar workflow steps to identify common patterns and groupings "
        "using TF-IDF + KMeans clustering."
    )

    def run(self, steps: list, num_clusters: int = 3) -> dict:
        """
        Args:
          steps: List of step descriptions (strings).
          num_clusters: Desired number of clusters.
        Returns:
          { "clusters": [ {"cluster_id": int, "steps": [str, ...] }, ... ] }
        """
        # Convert steps to TF-IDF vectors
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(steps)
        # KMeans clustering
        km = KMeans(n_clusters=min(num_clusters, len(steps)))
        labels = km.fit_predict(X)
        clusters = {}
        for step, label in zip(steps, labels):
            clusters.setdefault(label, []).append(step)
        return {"clusters": [{"cluster_id": k, "steps": v} for k, v in clusters.items()]}


class AnomalyDetectionTool(Tool):
    name = "anomaly_detection"
    description = (
        "Detects anomalous steps or outliers in the workflow sequence using Isolation Forest."
    )

    def run(self, steps: list) -> dict:
        """
        Args:
          steps: List of step descriptions (strings).
        Returns:
          { "anomalies": [str, ...] }  # steps flagged as unusual
        """
        # Simple numeric encoding: length of each step
        lengths = np.array([len(s) for s in steps]).reshape(-1, 1)
        iso = IsolationForest(contamination=0.1, random_state=42)
        preds = iso.fit_predict(lengths)
        anomalies = [step for step, p in zip(steps, preds) if p == -1]
        return {"anomalies": anomalies}


