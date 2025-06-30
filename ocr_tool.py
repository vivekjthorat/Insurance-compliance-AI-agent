import io
import pdfplumber
from PIL import Image

def ocr_tool(file_bytes, filename=None):
    """
    Extract text from PDF files using pdfplumber.
    Streamlit Cloud does not support image OCR (pytesseract), so fallback message for images.
    """
    is_pdf = (
        (filename and filename.lower().endswith('.pdf')) or
        file_bytes[:4] == b'%PDF'
    )

    if is_pdf:
        try:
            text = ""
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text() or ""
                    text += f"\n--- Page {i+1} ---\n{page_text}\n"
            return text.strip() or "❌ No readable text found in PDF."
        except Exception as e:
            print("❌ PDF text extraction failed:", e)
            return "❌ Error extracting text from PDF."
    else:
        # Image OCR fallback message
        return "❌ OCR for images is not supported on cloud. Please upload a PDF."
