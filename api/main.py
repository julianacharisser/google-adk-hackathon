import json
from orchestrators.business_process_agent import business_process_agent
import sys; print(sys.path)

def main():
    # 1) Path to SOP file (PDF/Word)
    sop_file = "sample-data/StyleHiveSOP.txt"

    # 2) Sector and business context
    params = {
      "file_path": sop_file,
      "sector": "Retail",
      "business_context": {
        "company_name": "Example SME",
        "staff_count": 10,
        "systems": ["CloudPOSX"],
        "compliance": ["ACRA","IRAS"]
      }
    }
    result = business_process_agent.run(params)
    print(json.dumps(result.content, indent=2))

if __name__ == "__main__":
    main()
