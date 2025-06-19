from google.adk.tools import Tool

class ROICalculatorTool(Tool):
    name = "roi_calculator"
    description = (
        "Calculates estimated time and cost savings, monthly savings, and payback period "
        "for a list of automation suggestions using rule-based formulas."
    )

    def run(self, items: list, hourly_cost: float = 18.0) -> dict:
        """
        Args:
          items: List of dicts, each containing:
            - step (str)
            - time_per_task_min (float)
            - frequency_per_month (int)
            - effort_multiplier (float)
            - feasibility_multiplier (float)
            - error_multiplier (float)
            - tool_multiplier (float)
            - implementation_cost (float, optional)
          hourly_cost: Staff cost per hour in SGD

        Returns:
          { "roi": [
              {"step": str, "estimated_savings_SGD": float, "payback_months": float}, ...
            ],
            "total_monthly_savings": float
          }
        """
        results = []
        total = 0.0
        for item in items:
            t_hours = item["time_per_task_min"] / 60.0
            freq = item["frequency_per_month"]
            mult = (
                item.get("effort_multiplier", 1.0)
                * item.get("feasibility_multiplier", 1.0)
                * item.get("error_multiplier", 1.0)
                * item.get("tool_multiplier", 1.0)
            )
            savings = t_hours * hourly_cost * freq * mult
            total += savings
            cost = item.get("implementation_cost", 1000)
            payback = cost / (savings + 1e-6)
            results.append({
                "step": item["step"],
                "estimated_savings_SGD": round(savings, 2),
                "payback_months": round(payback, 1)
            })
        return {"roi": results, "total_monthly_savings": round(total, 2)}