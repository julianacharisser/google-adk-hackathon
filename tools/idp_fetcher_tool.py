from google.adk.tools import Tool
import requests
import io
import pdfplumber

class IDPFetcherTool(Tool):
    name = "idp_fetcher"
    description = (
        "Fetch and extract the Industry Digital Plan (IDP) for a given sector from IMDA website."
    )

    def run(self, sector: str) -> str:
        # 1. Search for the IDP PDF URL (could integrate with google_search tool instead)
        query = f"site:imda.gov.sg idp {sector} PDF"
        # Here you might call google_search or a custom search API
        # For simplicity, assume we have a direct mapping or fixed URL
        pdf_url = f"https://www.imda.gov.sg/-/media/Imda/Files/Industry-Development/IDP/{sector}-IDP.pdf"

        # 2. Download the PDF
        resp = requests.get(pdf_url)
        resp.raise_for_status()
        fp = io.BytesIO(resp.content)

        # 3. Extract text using pdfplumber
        text = []
        with pdfplumber.open(fp) as pdf:
            for page in pdf.pages:
                txt = page.extract_text()
                if txt:
                    text.append(txt)
        return "\n".join(text)