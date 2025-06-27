import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
import io

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set Poppler path for Windows
POPLER_PATH = r"C:\poppler\poppler-24.08.0\Library\bin"

def extract_text_smart(file_bytes):
    """
    Extract text from a PDF using pdfplumber (text-based PDFs).
    If no text is found, fall back to OCR using pdf2image and pytesseract (scanned/image-based PDFs).
    Args:
        file_bytes (bytes): Raw PDF file bytes (e.g., from Streamlit uploader)
    Returns:
        str: Extracted and cleaned text from the PDF
    """
    text = ""
    # --- 1. Try extracting text with pdfplumber ---
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        # Clean up whitespace
        if text and text.strip():
            return text.strip()
    except Exception as e:
        print(f"[pdfplumber] Exception: {e}")

    # --- 2. Fallback: OCR each page image ---
    try:
        images = convert_from_bytes(file_bytes, poppler_path=POPLER_PATH)
        ocr_text = ""
        for i, img in enumerate(images):
            page_ocr = pytesseract.image_to_string(img)
            ocr_text += f"\n--- Page {i+1} ---\n" + page_ocr
        return ocr_text.strip()
    except Exception as e:
        print(f"[OCR fallback] Exception: {e}")
        return "" 