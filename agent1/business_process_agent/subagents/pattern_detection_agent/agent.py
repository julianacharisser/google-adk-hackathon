from google.adk.agents import Agent
from google.adk.tools import BaseTool
import typing
# from tools.pattern_tools import SequenceClusteringTool, AnomalyDetectionTool

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest


class SequenceClusteringTool(BaseTool):
    
    def __init__(self):
        super().__init__(
            name="SequenceClusteringTool",
            description="Clusters similar workflow steps to identify common patterns and groupings using TF-IDF + KMeans clustering"
        )
    
    def get_description(self) -> str:
        return "Clusters similar workflow steps to identify common patterns and groupings using TF-IDF + KMeans clustering"
    
    def get_parameters(self) -> typing.Dict:
        return {
            "steps": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of step descriptions to cluster"
            },
            "num_clusters": {
                "type": "integer",
                "default": 3,
                "description": "Desired number of clusters"
            }
        }

    def run(self, parameters: typing.Dict) -> typing.Dict:
        """
        Clusters workflow steps using TF-IDF and KMeans.
        """
        steps = parameters.get("steps", [])
        num_clusters = parameters.get("num_clusters", 3)
        
        if len(steps) < 2:
            return {"clusters": [{"cluster_id": 0, "steps": steps}]}
        
        try:
            # Convert steps to TF-IDF vectors
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(steps)
            # KMeans clustering
            km = KMeans(n_clusters=min(num_clusters, len(steps)), random_state=42)
            labels = km.fit_predict(X)
            clusters = {}
            for step, label in zip(steps, labels):
                clusters.setdefault(label, []).append(step)
            return {"clusters": [{"cluster_id": k, "steps": v} for k, v in clusters.items()]}
        except Exception as e:
            return {"error": f"Clustering failed: {str(e)}"}


class AnomalyDetectionTool(BaseTool):
    
    def __init__(self):
        super().__init__(
            name="AnomalyDetectionTool",
            description="Detects anomalous steps or outliers in the workflow sequence using Isolation Forest"
        )
    
    def get_description(self) -> str:
        return "Detects anomalous steps or outliers in the workflow sequence using Isolation Forest"
    
    def get_parameters(self) -> typing.Dict:
        return {
            "steps": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of step descriptions to analyze for anomalies"
            }
        }

    def run(self, parameters: typing.Dict) -> typing.Dict:
        """
        Detects anomalous steps using Isolation Forest.
        """
        steps = parameters.get("steps", [])
        
        if len(steps) < 3:
            return {"anomalies": []}
        
        try:
            # Simple numeric encoding: length of each step
            lengths = np.array([len(s) for s in steps]).reshape(-1, 1)
            iso = IsolationForest(contamination=0.1, random_state=42)
            preds = iso.fit_predict(lengths)
            anomalies = [step for step, p in zip(steps, preds) if p == -1]
            return {"anomalies": anomalies}
        except Exception as e:
            return {"error": f"Anomaly detection failed: {str(e)}"}

# —————————————————————————————
# 3) Sub-Agent: PatternDetectionAgent
# Identifies inefficiencies via sequence clustering and anomaly detection.
# —————————————————————————————
pattern_detection_agent = Agent(
    name="PatternDetectionAgent",
    model="gemini-2.0-flash",
    tools=[SequenceClusteringTool(), AnomalyDetectionTool()],
    description="Identifies workflow inefficiencies via clustering and anomaly detection from comprehensive process analysis",
    instruction="""
        **Role:**
        You are the Pattern Detection Agent. Your job is to identify additional inefficiencies and bottlenecks in a discovered workflow using advanced pattern analysis techniques.

        **Tools:**
        - `SequenceClusteringTool`: clusters similar steps to find recurrent patterns.
        - `AnomalyDetectionTool`: flags outlier steps that deviate from typical patterns.

        **Input:**
        A comprehensive JSON object from ProcessMiningAgent with the new format:
        ```json
        {
          "document_summary": {
            "title": "Daily Inventory Management Procedure",
            "doc_no": "SOP-INV-001",
            "version": "v2.1",
            "total_steps": 8
          },
          "process_map": [
            {
              "order": 1,
              "step_id": "1.0", 
              "step": "Begin Daily Inventory Audit",
              "actor": "Floor Staff",
              "type": "main_step",
              "estimated_duration": "5",
              "complexity": "low"
            },
            {
              "order": 2,
              "step_id": "1.1",
              "step": "Collect inventory sheets from storage room",
              "actor": "Floor Staff", 
              "type": "sub_step",
              "estimated_duration": "2",
              "complexity": "low"
            }
          ],
          "role_analysis": {
            "Floor Staff": {
              "total_steps": 3,
              "workload_percentage": "37.5",
              "key_responsibilities": ["Inventory collection", "Data entry"]
            }
          },
          "process_insights": {
            "bottlenecks": [
              {
                "step_id": "2.0",
                "issue": "Manual counting process is time-consuming",
                "impact": "high"
              }
            ],
            "optimization_opportunities": [
              {
                "category": "automation",
                "suggestion": "Implement barcode scanning",
                "expected_improvement": "50% reduction in counting time"
              }
            ]
          }
        }
        ```

        **Workflow:**
        1. Extract the list of `step` descriptions from the `process_map` array.
        2. Call `SequenceClusteringTool.run(steps)` to group similar steps and understand common patterns.
        3. Call `AnomalyDetectionTool.run(steps)` to detect any outlier or unusual steps.
        4. Analyze the existing `process_insights` to avoid duplicating already identified issues.
        5. Combine clustering and anomalies with role analysis to identify additional inefficiencies.

        **Task:**
        Return a JSON object with additional pattern-based insights:
        ```json
        {
          "pattern_analysis": {
            "step_clusters": [
              {
                "cluster_id": 0,
                "pattern_type": "manual_data_entry",
                "steps": ["step 1", "step 2"],
                "inefficiency_score": "high|medium|low",
                "automation_potential": "high|medium|low"
              }
            ],
            "workflow_anomalies": [
              {
                "step": "Monthly report generation",
                "anomaly_type": "frequency_outlier|duration_outlier|complexity_mismatch",
                "issue": "Step occurs infrequently but takes disproportionate time",
                "recommendation": "Automate or create template"
              }
            ],
            "role_imbalance_patterns": [
              {
                "role": "Floor Staff", 
                "pattern": "overloaded_with_manual_tasks",
                "affected_steps": ["1.1", "1.2", "2.3"],
                "suggestion": "Redistribute tasks or provide automation tools"
              }
            ]
          },
          "additional_optimizations": [
            {
              "category": "pattern_consolidation",
              "finding": "Multiple similar manual steps can be consolidated",
              "affected_steps": ["1.1", "1.2", "2.1"],
              "expected_improvement": "30% time reduction through step merging"
            }
          ],
          "quality_insights": {
            "process_consistency": "high|medium|low",
            "standardization_opportunities": [
              {
                "area": "data_entry_methods",
                "current_variation": "Different formats used across steps",
                "standardization_benefit": "Reduced errors and training time"
              }
            ]
          }
        }
        ```

        **Constraints:**
        - Focus on patterns not already identified in the input `process_insights`.
        - Maximum of 20 steps; if more, sample representative steps from each role.
        - Limit clusters to at most 5 for clarity.
        - Provide actionable recommendations based on detected patterns.
        - Consider role workload distribution when identifying inefficiencies.
    """,
)