from google.adk.agents import Agent
from google.adk.tools import google_search, BaseTool
import typing
import json

class GrantDatabaseTool(BaseTool):
    """
    Tool for searching Singapore's comprehensive grant database including 
    Enterprise Singapore, IMDA, and other government agency grants.
    """
    
    def __init__(self):
        super().__init__(
            name="GrantDatabaseTool",
            description="Searches Singapore's grant database for relevant funding opportunities"
        )
    
    def get_description(self) -> str:
        return "Searches Singapore's grant database for relevant funding opportunities"
    
    def get_parameters(self) -> typing.Dict:
        return {
            "sector": {
                "type": "string",
                "description": "Business sector (e.g., 'Retail', 'F&B', 'Manufacturing')",
                "required": False
            },
            "company_size": {
                "type": "string", 
                "description": "Company size ('Micro', 'Small', 'Medium')",
                "required": False
            },
            "funding_type": {
                "type": "string",
                "description": "Type of funding needed (e.g., 'Digital Transformation', 'Training')",
                "required": False
            },
            "keywords": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Additional search keywords",
                "required": False
            }
        }
    
    def run(self, parameters: typing.Dict) -> typing.Dict:
        """
        Search for grants based on company profile and requirements.
        """
        sector = parameters.get("sector")
        company_size = parameters.get("company_size") 
        funding_type = parameters.get("funding_type")
        keywords = parameters.get("keywords", [])
        
        try:
            # Implementation would connect to Singapore's grant databases
            # This is a comprehensive placeholder structure with realistic Singapore grants
            
            grants_db = [
                {
                    "grant_id": "PSG001",
                    "name": "Productivity Solutions Grant",
                    "agency": "Enterprise Singapore",
                    "category": "Digital Transformation",
                    "max_funding": 50000,
                    "co_funding_rate": 0.8,
                    "eligibility_criteria": [
                        "Singapore-registered company",
                        "Annual revenue between $30K-$100M",
                        "Implement pre-approved solutions"
                    ],
                    "application_url": "https://www.businessgrants.gov.sg/",
                    "deadline": "Ongoing",
                    "sectors": ["Retail", "F&B", "Manufacturing", "Services"],
                    "company_sizes": ["Micro", "Small", "Medium"]
                },
                {
                    "grant_id": "SFEC001", 
                    "name": "SkillsFuture Enterprise Credit",
                    "agency": "SkillsFuture Singapore",
                    "category": "Training & Development",
                    "max_funding": 10000,
                    "co_funding_rate": 1.0,
                    "eligibility_criteria": [
                        "Singapore-registered company",
                        "Train local employees"
                    ],
                    "application_url": "https://www.skillsfuture.gov.sg/",
                    "deadline": "31 Dec 2025",
                    "sectors": ["All"],
                    "company_sizes": ["All"]
                },
                {
                    "grant_id": "EDG001",
                    "name": "Enterprise Development Grant",
                    "agency": "Enterprise Singapore", 
                    "category": "Business Growth",
                    "max_funding": 1000000,
                    "co_funding_rate": 0.7,
                    "eligibility_criteria": [
                        "Singapore-registered company",
                        "Minimum 30% local shareholding",
                        "Business expansion or capability development"
                    ],
                    "application_url": "https://www.enterprisesg.gov.sg/",
                    "deadline": "Ongoing",
                    "sectors": ["Manufacturing", "Services", "Technology"],
                    "company_sizes": ["Small", "Medium"]
                },
                {
                    "grant_id": "ICV001",
                    "name": "Innovation & Capability Voucher",
                    "agency": "Enterprise Singapore",
                    "category": "Innovation",
                    "max_funding": 5000,
                    "co_funding_rate": 1.0,
                    "eligibility_criteria": [
                        "Singapore-registered company",
                        "Annual revenue up to $100M"
                    ],
                    "application_url": "https://www.enterprisesg.gov.sg/",
                    "deadline": "Ongoing",
                    "sectors": ["All"],
                    "company_sizes": ["Micro", "Small", "Medium"]
                }
            ]
            
            # Filter grants based on criteria
            filtered_grants = []
            for grant in grants_db:
                match = True
                
                if sector and sector not in grant["sectors"] and "All" not in grant["sectors"]:
                    match = False
                    
                if company_size and company_size not in grant["company_sizes"] and "All" not in grant["company_sizes"]:
                    match = False
                    
                if funding_type and funding_type.lower() not in grant["category"].lower():
                    match = False
                
                if match:
                    filtered_grants.append(grant)
            
            return {
                "grants_found": filtered_grants,
                "total_found": len(filtered_grants),
                "search_criteria": {
                    "sector": sector,
                    "company_size": company_size,
                    "funding_type": funding_type,
                    "keywords": keywords
                }
            }
            
        except Exception as e:
            return {"error": f"Grant database search failed: {str(e)}"}


class GrantEligibilityCheckerTool(BaseTool):
    """
    Tool for validating SME eligibility against specific grant criteria.
    """
    
    def __init__(self):
        super().__init__(
            name="GrantEligibilityCheckerTool",
            description="Validates company eligibility for specific grants"
        )
    
    def get_description(self) -> str:
        return "Validates company eligibility for specific grants"
    
    def get_parameters(self) -> typing.Dict:
        return {
            "grant_id": {
                "type": "string",
                "description": "Grant identifier to check eligibility for",
                "required": True
            },
            "company_profile": {
                "type": "object",
                "description": "Company information for eligibility check",
                "required": True,
                "properties": {
                    "annual_revenue": {"type": "number"},
                    "employee_count": {"type": "integer"},
                    "local_shareholding": {"type": "number"},
                    "years_in_operation": {"type": "integer"},
                    "sector": {"type": "string"},
                    "size": {"type": "string"}
                }
            }
        }
    
    def run(self, parameters: typing.Dict) -> typing.Dict:
        """
        Check eligibility for a specific grant.
        """
        grant_id = parameters.get("grant_id")
        company_profile = parameters.get("company_profile", {})
        
        try:
            # Implementation would validate against actual grant criteria
            # This provides realistic eligibility assessment
            
            annual_revenue = company_profile.get("annual_revenue", 0)
            employee_count = company_profile.get("employee_count", 0)
            local_shareholding = company_profile.get("local_shareholding", 0)
            years_in_operation = company_profile.get("years_in_operation", 0)
            sector = company_profile.get("sector", "")
            company_size = company_profile.get("size", "")
            
            # Basic eligibility rules for common Singapore grants
            eligibility_rules = {
                "PSG001": {
                    "min_revenue": 30000,
                    "max_revenue": 100000000,
                    "min_local_shareholding": 0,
                    "required_registration": "Singapore",
                    "complexity_score": 0.6
                },
                "SFEC001": {
                    "min_revenue": 0,
                    "max_revenue": float('inf'),
                    "min_local_shareholding": 0,
                    "required_registration": "Singapore", 
                    "complexity_score": 0.2
                },
                "EDG001": {
                    "min_revenue": 100000,
                    "max_revenue": float('inf'),
                    "min_local_shareholding": 30,
                    "required_registration": "Singapore",
                    "complexity_score": 0.8
                },
                "ICV001": {
                    "min_revenue": 0,
                    "max_revenue": 100000000,
                    "min_local_shareholding": 0,
                    "required_registration": "Singapore",
                    "complexity_score": 0.3
                }
            }
            
            rules = eligibility_rules.get(grant_id, {})
            if not rules:
                return {"error": f"Unknown grant ID: {grant_id}"}
            
            # Check eligibility criteria
            eligible = True
            met_criteria = []
            missing_criteria = []
            eligibility_score = 1.0
            
            # Revenue check
            if annual_revenue < rules.get("min_revenue", 0):
                eligible = False
                missing_criteria.append(f"Minimum revenue of ${rules['min_revenue']:,}")
                eligibility_score -= 0.3
            else:
                met_criteria.append("Revenue requirement met")
                
            if annual_revenue > rules.get("max_revenue", float('inf')):
                eligible = False
                missing_criteria.append(f"Maximum revenue of ${rules['max_revenue']:,}")
                eligibility_score -= 0.3
            
            # Local shareholding check
            if local_shareholding < rules.get("min_local_shareholding", 0):
                eligible = False
                missing_criteria.append(f"Minimum {rules['min_local_shareholding']}% local shareholding")
                eligibility_score -= 0.2
            else:
                met_criteria.append("Local shareholding requirement met")
            
            # Always assume Singapore registration for this example
            met_criteria.append("Singapore-registered company")
            
            # Calculate success probability based on eligibility and complexity
            if eligible:
                success_rate = min(0.95, eligibility_score * (1 - rules.get("complexity_score", 0.5)))
            else:
                success_rate = 0.1  # Low chance if not eligible
            
            recommendations = []
            if missing_criteria:
                recommendations.extend([
                    f"Address missing criteria: {', '.join(missing_criteria)}",
                    "Consider consulting with grant application specialists"
                ])
            else:
                recommendations.extend([
                    "Prepare required documentation",
                    "Ensure compliance with grant conditions",
                    "Consider timing of application with business needs"
                ])
            
            return {
                "grant_id": grant_id,
                "eligible": eligible,
                "eligibility_score": round(max(0, eligibility_score), 2),
                "met_criteria": met_criteria,
                "missing_criteria": missing_criteria,
                "recommendations": recommendations,
                "estimated_success_rate": round(success_rate, 2)
            }
            
        except Exception as e:
            return {"error": f"Eligibility check failed: {str(e)}"}

# —————————————————————————————
# Sub-Agent: GrantMatchingAgent
# Identifies and matches SMEs with relevant government grants and funding opportunities
# —————————————————————————————

root_agent = Agent(
    name="GrantMatchingAgent", 
    model="gemini-2.0-flash",
    tools=[google_search, GrantDatabaseTool(), GrantEligibilityCheckerTool()],
    description="Identifies and matches SMEs with relevant grants and funding opportunities in Singapore",
    instruction="""
**Role:**
You are the Grant Matching Agent, specializing in identifying and matching SMEs with relevant government grants, funding schemes, and financial incentives available in Singapore.

**Tools:**
- `GrantDatabaseTool`: searches Singapore's comprehensive grant database including Enterprise Singapore, IMDA, and other agency grants
- `GrantEligibilityCheckerTool`: validates SME eligibility against specific grant criteria
- `google_search`: finds latest grant information, updates, and application details

**Input:**
A JSON object containing company profile and business needs:
```json
{
    "company_profile": {
        "name": "string",
        "sector": "string", // e.g., "Retail", "F&B", "Manufacturing"
        "size": "string", // e.g., "Micro", "Small", "Medium"
        "annual_revenue": "float", // in SGD
        "employee_count": "int",
        "business_stage": "string", // e.g., "Startup", "Growth", "Mature"
        "years_in_operation": "int",
        "local_shareholding": "float" // percentage
    },
    "business_needs": {
        "expansion_plans": "string",
        "technology_requirements": "array",
        "hiring_plans": "string",
        "equipment_needs": "array",
        "training_requirements": "array",
        "market_expansion": "string",
        "sustainability_goals": "string"
    },
    "funding_requirements": {
        "amount_needed": "float",
        "purpose": "string",
        "timeline": "string",
        "co_funding_capability": "float" // percentage company can contribute
    }
}
```

**Workflow:**
1. Analyze company profile to determine grant categories and eligibility
2. Use `GrantDatabaseTool.search()` to find relevant grants based on sector, size, and needs
3. For each potential grant, use `GrantEligibilityCheckerTool.check()` to validate eligibility
4. Use `google_search` to find latest grant updates, deadlines, and application procedures
5. Rank grants by relevance, funding amount, and probability of success
6. Create grant Eligibility Checklist 
6. Create a comprehensive grant strategy including immediate and future applications
7. Identify any eligibility gaps and recommend steps to qualify
8. The final output should not be json

**Task:**
Return a JSON object with matched grants and recommendations:
```json
{
    "matched_grants": [
        {
            "grant_name": "string",
            "agency": "string", // e.g., "Enterprise Singapore", "IMDA"
            "category": "string", // e.g., "Digital Transformation", "Capability Development"
            "funding_amount": "float", // maximum grant amount
            "co_funding_required": "float", // percentage company must contribute
            "eligibility_score": "float", // 0-1 score of eligibility match
            "application_complexity": "Low/Medium/High",
            "processing_time": "string", // typical approval timeframe
            "application_deadline": "string",
            "key_requirements": "array",
            "success_probability": "float" // 0-1 estimate
        }
    ],
    "grant_strategy": {
        "immediate_applications": "array", // grants to apply for immediately
        "pipeline_applications": "array", // grants for future consideration
        "total_potential_funding": "float",
        "recommended_sequence": "array" // optimal order of applications
    },
    "eligibility_gaps": [
        {
            "grant_name": "string",
            "missing_requirements": "array",
            "steps_to_qualify": "array",
            "timeline_to_qualify": "string"
        }
    ],
    "application_support": {
        "consultancy_grants": "array", // grants that provide application support
        "recommended_consultants": "array",
        "estimated_application_costs": "float"
    }
}
```

**Example Output:**
```json
{
    "matched_grants": [
        {
            "grant_name": "Productivity Solutions Grant (PSG)",
            "agency": "Enterprise Singapore",
            "category": "Digital Transformation",
            "funding_amount": 50000.0,
            "co_funding_required": 0.2,
            "eligibility_score": 0.95,
            "application_complexity": "Medium",
            "processing_time": "3-4 months",
            "application_deadline": "Ongoing",
            "key_requirements": ["Local company", "Implement pre-approved solutions", "Maintain employment"],
            "success_probability": 0.85
        },
        {
            "grant_name": "SkillsFuture Enterprise Credit",
            "agency": "SkillsFuture Singapore",
            "category": "Training & Development",
            "funding_amount": 10000.0,
            "co_funding_required": 0.0,
            "eligibility_score": 1.0,
            "application_complexity": "Low",
            "processing_time": "1-2 months",
            "application_deadline": "31 Dec 2024",
            "key_requirements": ["Singapore-registered company", "Training for employees"],
            "success_probability": 0.95
        }
    ],
    "grant_strategy": {
        "immediate_applications": ["SkillsFuture Enterprise Credit", "Productivity Solutions Grant"],
        "pipeline_applications": ["Innovation & Capability Voucher", "Enterprise Development Grant"],
        "total_potential_funding": 150000.0,
        "recommended_sequence": ["SkillsFuture first (quick approval)", "PSG for digital transformation", "ICV for innovation projects"]
    },
    "eligibility_gaps": [
        {
            "grant_name": "Scale-up SG",
            "missing_requirements": ["Minimum 3 years track record", "Revenue > SGD 1M"],
            "steps_to_qualify": ["Operate for 1 more year", "Increase revenue through expansion"],
            "timeline_to_qualify": "12-18 months"
        }
    ],
    "application_support": {
        "consultancy_grants": ["Innovation & Capability Voucher"],
        "recommended_consultants": ["SPRING Consultants", "Digital Transformation Partners"],
        "estimated_application_costs": 5000.0
    }
}
```

**Constraints:**
- Focus on Singapore government grants and schemes
- Maximum of 5 matched grants to avoid overwhelming the applicant
- Eligibility scores must be based on actual grant criteria
- Success probability estimates should be conservative and realistic
- Include both immediate and long-term grant opportunities
- Consider grant stacking opportunities (multiple grants for same project)
- Account for grant application timelines and business cash flow needs
- Prioritize grants with higher success rates and lower complexity for SMEs
- Include sector-specific grants (e.g., F&B, retail, manufacturing)
- Consider business stage appropriateness (startup vs. mature company grants)
""",
)
