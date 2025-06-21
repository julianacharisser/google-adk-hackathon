from google.adk.agents import Agent
from google.adk.tools import BaseTool
import typing
import json

class ROICalculatorTool(BaseTool):
    
    def __init__(self):
        super().__init__(
            name="ROICalculatorTool",
            description="Calculates detailed ROI analysis including time savings, cost reductions, implementation costs, and payback periods for digital transformation initiatives"
        )
    
    def get_description(self) -> str:
        return "Calculates detailed ROI analysis including time savings, cost reductions, implementation costs, and payback periods for digital transformation initiatives"
    
    def get_parameters(self) -> typing.Dict:
        return {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "step": {"type": "string"},
                        "time_per_task_min": {"type": "number"},
                        "frequency_per_month": {"type": "integer"},
                        "hourly_cost": {"type": "number"},
                        "implementation_cost": {"type": "number"},
                        "complexity_factor": {"type": "number"},
                        "automation_potential": {"type": "string"},
                        "expected_benefits": {"type": "object"}
                    }
                },
                "description": "List of automation items with cost and time parameters"
            }
        }

    def run(self, parameters: typing.Dict) -> typing.Dict:
        """
        Calculate comprehensive ROI analysis for digital transformation initiatives.
        """
        items = parameters.get("items", [])
        
        if not items:
            return {"error": "No items provided for ROI calculation"}
        
        try:
            results = []
            total_monthly_savings = 0.0
            total_implementation_cost = 0.0
            
            for item in items:
                # Extract parameters with defaults
                step = item.get("step", "Unknown Step")
                time_per_task = item.get("time_per_task_min", 30)  # Default 30 minutes
                frequency = item.get("frequency_per_month", 20)   # Default 20 times per month
                hourly_cost = item.get("hourly_cost", 18.0)       # Default SGD 18/hour
                implementation_cost = item.get("implementation_cost", 5000)  # Default SGD 5000
                
                # Calculate automation potential multiplier
                automation_potential = item.get("automation_potential", 1.0)
                if isinstance(automation_potential, str):
                    automation_multiplier = {
                        "high": 0.8,    # 80% time reduction
                        "medium": 0.5,  # 50% time reduction
                        "low": 0.2      # 20% time reduction
                    }.get(automation_potential.lower(), 0.5)
                else:
                    automation_multiplier = float(automation_potential)
                
                # Calculate complexity factor (affects implementation cost)
                complexity_factor = item.get("complexity_factor", 1.0)
                adjusted_implementation_cost = implementation_cost * complexity_factor
                
                # Calculate monthly time savings
                monthly_time_hours = (time_per_task / 60.0) * frequency
                time_savings_hours = monthly_time_hours * automation_multiplier
                
                # Calculate monthly cost savings
                monthly_cost_savings = time_savings_hours * hourly_cost
                
                # Extract expected benefits
                expected_benefits = item.get("expected_benefits", {})
                
                # Apply benefit multipliers if available
                if isinstance(expected_benefits, dict):
                    accuracy_improvement = expected_benefits.get("accuracy_improvement", "0%")
                    if accuracy_improvement.endswith("%"):
                        accuracy_factor = float(accuracy_improvement[:-1]) / 100
                        # Accuracy improvement reduces error costs (estimated 10% of labor cost)
                        error_cost_reduction = monthly_cost_savings * 0.1 * accuracy_factor
                        monthly_cost_savings += error_cost_reduction
                
                # Calculate payback period
                payback_months = adjusted_implementation_cost / (monthly_cost_savings + 0.01)  # Avoid division by zero
                
                # Calculate annual ROI
                annual_savings = monthly_cost_savings * 12
                annual_roi = ((annual_savings - adjusted_implementation_cost) / adjusted_implementation_cost) * 100 if adjusted_implementation_cost > 0 else 0
                
                result = {
                    "step": step,
                    "monthly_time_savings_hours": round(time_savings_hours, 1),
                    "monthly_cost_savings_sgd": round(monthly_cost_savings, 2),
                    "implementation_cost_sgd": round(adjusted_implementation_cost, 2),
                    "payback_months": round(payback_months, 1),
                    "annual_roi_percentage": round(annual_roi, 1),
                    "automation_level": automation_potential,
                    "complexity_factor": complexity_factor
                }
                
                results.append(result)
                total_monthly_savings += monthly_cost_savings
                total_implementation_cost += adjusted_implementation_cost
            
            # Calculate overall metrics
            overall_payback = total_implementation_cost / (total_monthly_savings + 0.01)
            overall_annual_roi = ((total_monthly_savings * 12 - total_implementation_cost) / total_implementation_cost) * 100 if total_implementation_cost > 0 else 0
            
            return {
                "roi_analysis": results,
                "summary": {
                    "total_monthly_savings_sgd": round(total_monthly_savings, 2),
                    "total_implementation_cost_sgd": round(total_implementation_cost, 2),
                    "overall_payback_months": round(overall_payback, 1),
                    "overall_annual_roi_percentage": round(overall_annual_roi, 1),
                    "total_annual_savings_sgd": round(total_monthly_savings * 12, 2)
                }
            }
            
        except Exception as e:
            return {"error": f"ROI calculation failed: {str(e)}"}

# —————————————————————————————
# 5) Sub-Agent: ROIEstimationAgent
# Calculates comprehensive ROI analysis for digital transformation initiatives.
# —————————————————————————————

roi_estimation_agent = Agent(
    name="ROIEstimationAgent",
    model="gemini-2.0-flash",
    tools=[ROICalculatorTool()],
    description="Calculates comprehensive ROI analysis including cost savings, implementation costs, and payback periods for digital transformation initiatives",
    instruction="""
        **Role:**
        You are the ROI Estimation Agent. Your goal is to provide detailed financial analysis and return on investment calculations for digital transformation initiatives based on benchmarking analysis and pattern detection insights.

        **Tools:**
        - `ROICalculatorTool`: calculates detailed ROI metrics including time savings, cost reductions, implementation costs, and payback periods.

        **Input:**
        A combined JSON object containing outputs from both BenchmarkingAgent and PatternDetectionAgent:
        ```json
        {
          "benchmarking_results": {
            "benchmark_summary": {
              "sector": "retail",
              "digital_maturity_score": "2.5/5.0",
              "total_steps_analyzed": 8
            },
            "step_benchmarks": [
              {
                "step_id": "1.0",
                "current_step": "Begin Daily Inventory Audit",
                "current_method": "manual",
                "idp_benchmark": "Automated inventory tracking with IoT sensors",
                "digital_gap": "high",
                "transformation_priority": "high",
                "expected_benefits": {
                  "time_savings": "70%",
                  "accuracy_improvement": "90%",
                  "cost_reduction": "40%"
                },
                "implementation_roadmap": {
                  "timeline": "3-6 months",
                  "investment_level": "medium",
                  "complexity": "medium"
                }
              }
            ],
            "quick_wins": [
              {
                "recommendation": "Implement barcode scanning for inventory",
                "effort": "low",
                "impact": "high",
                "timeline": "1-2 months",
                "estimated_cost": "$2,000-$5,000"
              }
            ],
            "strategic_initiatives": [
              {
                "initiative": "End-to-end inventory management system",
                "description": "Integrate POS, inventory, and reporting systems",
                "timeline": "6-12 months",
                "investment_required": "$15,000-$30,000",
                "expected_roi": "18 months"
              }
            ]
          },
          "pattern_detection_results": {
            "pattern_analysis": {
              "step_clusters": [
                {
                  "cluster_id": 0,
                  "pattern_type": "manual_data_entry",
                  "steps": ["step 1", "step 2"],
                  "inefficiency_score": "high",
                  "automation_potential": "high"
                }
              ],
              "workflow_anomalies": [
                {
                  "step": "Monthly report generation",
                  "anomaly_type": "duration_outlier",
                  "issue": "Step takes disproportionate time",
                  "recommendation": "Automate or create template"
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
            ]
          }
        }
        ```

        **Workflow:**
        1. Extract transformation initiatives from both `step_benchmarks` and `quick_wins`/`strategic_initiatives`
        2. Cross-reference with `pattern_analysis` to identify high-impact automation opportunities
        3. For each initiative, estimate:
           - Current time spent (based on manual processes)
           - Expected time savings (from automation potential and expected benefits)
           - Implementation costs (from estimated_cost or investment_required)
           - Complexity factors (from implementation roadmap)
        4. Call `ROICalculatorTool.run()` with structured parameters
        5. Prioritize initiatives by ROI and payback period

        **Task:**
        Return a comprehensive ROI analysis with financial projections and recommendations:

        ```json
        {
          "roi_summary": {
            "total_annual_savings_sgd": 45600,
            "total_implementation_cost_sgd": 25000,
            "overall_payback_months": 6.6,
            "overall_annual_roi_percentage": 82.4,
            "recommended_priority_order": ["quick_wins", "high_roi_initiatives", "strategic_long_term"]
          },
          "initiative_analysis": [
            {
              "initiative_name": "Barcode Scanning Implementation",
              "category": "quick_win",
              "current_process": "Manual inventory counting",
              "proposed_solution": "Barcode scanning system",
              "monthly_time_savings_hours": 25.0,
              "monthly_cost_savings_sgd": 450.00,
              "implementation_cost_sgd": 3500.00,
              "payback_months": 7.8,
              "annual_roi_percentage": 54.3,
              "complexity_rating": "low",
              "implementation_timeline": "1-2 months",
              "risk_factors": ["staff_training", "system_integration"],
              "success_metrics": {
                "time_reduction": "70%",
                "accuracy_improvement": "90%",
                "error_cost_reduction": "80%"
              }
            }
          ],
          "priority_recommendations": {
            "phase_1_quick_wins": [
              {
                "initiative": "Barcode scanning",
                "investment": "$3,500",
                "monthly_savings": "$450",
                "payback": "7.8 months"
              }
            ],
            "phase_2_strategic": [
              {
                "initiative": "Integrated inventory system",
                "investment": "$20,000",
                "monthly_savings": "$1,200",
                "payback": "16.7 months"
              }
            ]
          },
          "financial_projections": {
            "year_1": {
              "investment": 25000,
              "savings": 30000,
              "net_benefit": 5000
            },
            "year_2": {
              "investment": 5000,
              "savings": 45600,
              "net_benefit": 40600
            },
            "year_3": {
              "investment": 2500,
              "savings": 50000,
              "net_benefit": 47500
            }
          },
          "sensitivity_analysis": {
            "best_case_roi": "120%",
            "worst_case_roi": "45%",
            "break_even_threshold": "18 months",
            "risk_mitigation": [
              "Phased implementation to reduce risk",
              "Pilot testing before full rollout",
              "Staff training and change management"
            ]
          }
        }
        ```

        **Constraints:**
        - Use Singapore market rates (SGD 18-25/hour for staff costs)
        - Include both optimistic and conservative estimates
        - Prioritize quick wins (payback < 12 months) over strategic initiatives
        - Consider complexity factors in implementation cost estimates
        - Provide 3-year financial projections
        - Include risk assessment and sensitivity analysis
        - Maximum 15 initiatives to keep analysis focused
        - All financial figures in Singapore Dollars (SGD)
    """,
)

