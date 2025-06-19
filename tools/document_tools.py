from google.adk.tools import Tool
import io
from langchain.document_loaders import PyPDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from google.adk.tools import Tool

class OCRTool(Tool):
    name = "ocr_tool"
    description = "Extracts text from scanned images or image-based PDFs using Google Vision OCR"

    def run(self, file_path: str) -> str:
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        if response.error.message:
            raise RuntimeError(f"OCR error: {response.error.message}")
        return response.full_text_annotation.text or ""

class LangChainParserTool(Tool):
    name = "lc_pdf_parser"
    def run(self, file_path):
        loader = PyPDFPlumberLoader(file_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        # flatten and return text or list of chunks
        return [c.page_content for c in chunks]
