import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
from pdf2image import convert_from_bytes
import os

# Set Tesseract path - works on both Windows and Linux
# On Windows: C:\Program Files\Tesseract-OCR\tesseract.exe
# On Linux (Streamlit Cloud): /usr/bin/tesseract
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# On Linux, tesseract is usually in PATH, so no need to set it

def preprocess_image(image_bytes):
    """
    Preprocess image for OCR: grayscale and thresholding.
    Args:
        image_bytes (bytes): Image file in bytes.
    Returns:
        np.ndarray: Preprocessed image.
    """
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img_np = np.array(image)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def ocr_tool(file_bytes, filename=None):
    """
    Run OCR on image or PDF. If PDF, convert all pages to images and OCR each.
    Args:
        file_bytes (bytes): File in bytes.
        filename (str): Optional filename for extension check.
    Returns:
        str: Extracted text from all pages/images.
    """
    # Detect file type
    is_pdf = (
        (filename and filename.lower().endswith('.pdf')) or
        file_bytes[:4] == b'%PDF'
    )

    if is_pdf:
        try:
            # On Streamlit Cloud, poppler is installed in /usr/bin
            images = convert_from_bytes(file_bytes)
        except Exception as e:
            print("❌ PDF to image conversion failed:", e)
            return ""

        text = ""
        for i, page_img in enumerate(images):
            img_np = np.array(page_img.convert('RGB'))
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            page_text = pytesseract.image_to_string(thresh)
            text += f"\n--- Page {i+1} ---\n" + page_text

        return text.strip()

    else:
        preprocessed = preprocess_image(file_bytes)
        text = pytesseract.image_to_string(preprocessed)
        return text.strip()
