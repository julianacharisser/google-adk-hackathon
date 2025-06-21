from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import BaseTool
import requests
import io
import typing

try:
    import pdfplumber
except ImportError:
    print("⚠️ Warning: pdfplumber not installed. Install with: pip install pdfplumber")
    pdfplumber = None

class IDPFetcherTool(BaseTool):
    
    def __init__(self):
        super().__init__(
            name="IDPFetcherTool",
            description="Fetch and extract the Industry Digital Plan (IDP) for a given sector from IMDA website"
        )
    
    def get_description(self) -> str:
        return "Fetch and extract the Industry Digital Plan (IDP) for a given sector from IMDA website"
    
    def get_parameters(self) -> typing.Dict:
        return {
            "sector": {
                "type": "string",
                "description": "The industry sector (e.g., 'retail', 'manufacturing', 'food_services')"
            }
        }

    def run(self, parameters: typing.Dict) -> typing.Dict:
        """
        Fetch and extract the Industry Digital Plan (IDP) for a given sector.
        """
        sector = parameters.get("sector", "").lower()
        
        if not sector:
            return {"error": "Sector parameter is required"}
        
        try:
            # 1. Construct IDP PDF URL (based on common IMDA URL patterns)
            pdf_url = f"https://www.imda.gov.sg/-/media/Imda/Files/Industry-Development/IDP/{sector}-IDP.pdf"

            # 2. Download the PDF
            resp = requests.get(pdf_url, timeout=30)
            resp.raise_for_status()
            
            if not pdfplumber:
                return {"error": "pdfplumber not available for PDF processing"}
            
            fp = io.BytesIO(resp.content)

            # 3. Extract text using pdfplumber
            text_content = []
            with pdfplumber.open(fp) as pdf:
                for page in pdf.pages:
                    txt = page.extract_text()
                    if txt:
                        text_content.append(txt)
            
            full_text = "\n".join(text_content)
            
            return {
                "sector": sector,
                "source_url": pdf_url,
                "content": full_text[:10000],  # Limit to first 10k chars to avoid token limits
                "content_length": len(full_text),
                "pages_extracted": len(text_content)
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to download IDP document: {str(e)}"}
        except Exception as e:
            return {"error": f"IDP processing failed: {str(e)}"}
    
# —————————————————————————————
# 4) Sub-Agent: BenchmarkingAgent
# Compares metrics against industry norms using IDP sector data.
# —————————————————————————————

benchmarking_agent = Agent(
    name="BenchmarkingAgent",
    model="gemini-2.0-flash",
    tools=[google_search, IDPFetcherTool()],
    description="Compares workflow processes against Singapore IDP digital transformation benchmarks and best practices",
    instruction="""
        **Role:**
        You are the Benchmarking Agent. Your job is to compare a company's discovered workflow processes against Singapore's Industry Digital Plan (IDP) best practices and digital transformation benchmarks for their sector.
        
        **Tools:**
        - `IDPFetcherTool`: fetches and extracts the full text of the IMDA IDP PDF for the target sector.
        - `google_search`: to locate related IDP guidance or sector-specific resources online.
        
        **Input:**
        A combined JSON object containing outputs from both ProcessMiningAgent and PatternDetectionAgent:
        ```json
        {
          "company_info": {
            "sector": "retail",
            "company_size": "sme"
          },
          "process_mining_results": {
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
                "expected_improvement": "30% time reduction"
              }
            ]
          }
        }
        ```
        
        **Workflow:**
        1. Extract the sector from `company_info.sector`
        2. Use `IDPFetcherTool.run({"sector": sector})` to retrieve the IDP content for that sector
        3. Optionally use `google_search` to find additional IMDA resources or sector-specific guidelines
        4. Analyze the `process_map` steps against IDP digital transformation recommendations
        5. Cross-reference with `pattern_detection_results` to identify high-priority improvement areas
        6. Focus on steps that have:
           - High automation potential from pattern analysis
           - Identified bottlenecks from process insights
           - Clear digital transformation opportunities in the IDP
        
        **Task:**
        Return a comprehensive benchmarking analysis with actionable digital transformation recommendations:
        
        ```json
        {
          "benchmark_summary": {
            "sector": "retail",
            "idp_version": "2024",
            "total_steps_analyzed": 8,
            "digital_maturity_score": "2.5/5.0",
            "priority_areas": ["inventory_management", "reporting_automation", "data_integration"]
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
                "phase": "1",
                "timeline": "3-6 months",
                "investment_level": "medium",
                "complexity": "medium"
              }
            }
          ],
          "role_transformation_analysis": {
            "Floor Staff": {
              "current_workload": "37.5%",
              "tasks_for_automation": ["manual counting", "data entry"],
              "future_role_focus": ["exception handling", "quality assurance"],
              "upskilling_requirements": ["digital tools training", "data analysis basics"]
            }
          },
          "idp_alignment_score": {
            "overall_score": "35%",
            "areas": {
              "process_digitization": "25%",
              "data_integration": "40%", 
              "automation_adoption": "30%",
              "digital_skills": "45%"
            }
          },
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
        }
        ```

        **Constraints:**
        - Limit to maximum 15 step benchmarks for clarity
        - Prioritize steps with highest automation potential and business impact
        - All recommendations must be grounded in actual IDP content or official IMDA guidelines
        - Include specific cost estimates and timelines where possible
        - Focus on SME-appropriate solutions (not enterprise-scale implementations)
        - Provide both quick wins (3-6 months) and strategic initiatives (6-18 months)
    """,
)

