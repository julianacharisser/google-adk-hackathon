from google.adk.agents import Agent
from google.adk.tools import BaseTool
import typing
import io
try:
    from langchain_community.document_loaders import PyPDFLoader
except ImportError:
    try:
        from langchain.document_loaders import PyPDFLoader
    except ImportError:
        PyPDFLoader = None
from langchain.text_splitter import RecursiveCharacterTextSplitter

class OCRTool(BaseTool):
    
    def __init__(self):
        super().__init__(
            name="OCRTool",
            description="Extracts text from scanned images or image-based PDFs using Google Vision OCR"
        )
    
    def get_description(self) -> str:
        return "Extracts text from scanned images or image-based PDFs using Google Vision OCR"
    
    def get_parameters(self) -> typing.Dict:
        return {
            "file_path": {
                "type": "string",
                "description": "Path to the image or PDF file to extract text from"
            }
        }

    def run(self, parameters: typing.Dict) -> typing.Dict:
        file_path = parameters.get("file_path")
        try:
            from google.cloud import vision
            client = vision.ImageAnnotatorClient()
            with io.open(file_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = client.document_text_detection(image=image)
            if response.error.message:
                raise RuntimeError(f"OCR error: {response.error.message}")
            extracted_text = response.full_text_annotation.text or ""
            return {"extracted_text": extracted_text}
        except Exception as e:
            return {"error": f"OCR processing failed: {str(e)}"}

class LangChainParserTool(BaseTool):
    
    def __init__(self):
        super().__init__(
            name="LangChainParserTool", 
            description="Parses machine-readable PDFs and splits into chunks"
        )
    
    def get_description(self) -> str:
        return "Parses machine-readable PDFs and splits into chunks using PyPDFPlumberLoader"
    
    def get_parameters(self) -> typing.Dict:
        return {
            "file_path": {
                "type": "string", 
                "description": "Path to the PDF file to parse"
            }
        }
    
    def run(self, parameters: typing.Dict) -> typing.Dict:
        file_path = parameters.get("file_path")
        try:
            if PyPDFLoader is None:
                return {"error": "PDF parsing libraries not available. Please install: pip install langchain-community pypdf"}
            
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)
            chunk_texts = [c.page_content for c in chunks]
            return {"chunks": chunk_texts, "raw_text": " ".join(chunk_texts)}
        except Exception as e:
            return {"error": f"PDF parsing failed: {str(e)}. Try installing: pip install langchain-community pypdf"}

# —————————————————————————————
# 1) Sub-Agent: DocumentIngestionAgent
# OCR and PDF/text parser for unstructured process documents.
# —————————————————————————————
document_ingestion_agent = Agent(
    name="DocumentIngestionAgent",
    model="gemini-2.0-flash",
    tools=[
        OCRTool(),          # Converts scanned PDFs/images to raw text
        LangChainParserTool(),   # Parses text from digital PDFs, Word documents, and plain text files
    ],
    description="Parses SOP docs and returns raw-text + initial step list",
    instruction="""
        **Role:**
        You are the "SOP Ingestion Engine", a specialized AI agent responsible for accurately extracting and structuring text from Standard Operating Procedure (SOP) documents.

        **Your Persona:**
        You are a meticulous and efficient data processor. Your communication should be direct and clear, especially when reporting success or errors.

        **Tools:**
        - `FileTypeDetectorTool`: Analyzes a file and determines if it is "digital" (text-based PDF/DOCX) or "scanned" (image-based PDF/JPG/PNG).
        - `DigitalParserTool`: Extracts and chunks text from digital PDF and DOCX files. Returns a list of text chunks.
        - `OCRParserTool`: Extracts and chunks text from scanned images and image-based PDFs. Returns a list of text chunks.

        **Input:**
        The user will provide a path to a company’s Standard Operating Procedure (SOP) file.
            
        **Before you start:**
        -Always read the **Workflow** section carefully.

        **Workflow:** 
        1.  **Always start by calling the `FileTypeDetectorTool`** with the user's file path to determine the document type.
        2.  Based on the detector's output:
            - If the type is "digital", you **MUST** call the `DigitalParserTool`.
            - If the type is "scanned", you **MUST** call the `OCRParserTool`.
        3. **Structuring (CRITICAL NEW STEP):** After you have the raw text, your main task begins. 
            You must **analyze the content of the `raw_text`** to identify its semantic structure. Look for headings like "Purpose," "Scope," "Risk Assessment," and "Procedure." 
            Within the procedure, identify the main steps, sub-steps, and the roles responsible (e.g., "Floor Staff," "Inventory Clerk").
        4. **Output Generation:** Transform your analysis from the previous step into a single, detailed, hierarchical JSON object that strictly follows the "Final Hierarchical Output Schema" provided below.
        4.  If any tool fails or no text can be extracted, return an error message in the specified format.

        **Task:**  
        Your final output MUST be a single JSON object that strictly follows the hierarchical schema. **Do not return the old flat list of `steps`.** The goal is to create a structured representation of the document's content.
        
        **Success Final Hierarchical Output Schema:**
        ```
        {
          "title": "<The document title>",
          "document_info": {
            "doc_no": "<Document Number>",
            "version": "<Version>",
            "date": "<Date>"
          },
          "sections": {
            "purpose": "<The text from the purpose section>",
            "scope": "<The text from the scope section>",
            "risk_assessment": {
              "risks": ["<risk 1>", "<risk 2>", "..."],
              "mitigations": ["<mitigation 1>", "<mitigation 2>", "..."]
            },
            "procedure": [
              {
                "step_number": "<e.g., '1'>",
                "title": "<The title of the main step, e.g., 'Begin Inventory Audit'>",
                "role": "<The role responsible, e.g., 'Floor Staff'>",
                "sub_steps": ["<sub_step 1.1>", "<sub_step 1.2>", "..."]
              }
            ]
          }
        }
        ```

        **Error Output Schema:**
        If any tool fails or no text can be extracted, you must return a JSON object in this format:
        ```
        {
            "status": "error",
            "error_message": "<A brief description of the error, e.g., 'Failed to extract text from scanned document.' or 'File type is not supported.'>"
        }
        ```

        **Constraints:**
       You must operate within the following system limits. The tools are designed to enforce these rules and will report an error if a constraint is violated.
        1. **Supported formats:** PDF, DOCX, TXT, JPG, PNG.
        2. **Maximum file size:** 20 MB per request.
        3. **Maximum document length:** 50 pages or ~100,000 characters.
        4. **OCR Accuracy:** OCR accuracy may drop on low-resolution scans. If no text is extracted, this is considered an error.
        5. **Chunk Size:** The parser tools will automatically ensure that each text chunk is ≤1000 tokens to fit within the context window. You do not need to perform this chunking yourself.
    """,)
