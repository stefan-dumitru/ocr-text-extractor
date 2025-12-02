import os
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Stefan Dumitru\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
import pdfplumber
from pdf2image import convert_from_path

from .handwriting_service import extract_handwriting_text

def extract_text_from_file(filepath):
    text = ""

    # check file extension
    ext = os.path.splitext(filepath)[1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(thresh, lang='eng+ron')

        if len(text.strip()) < 5:  
            handwriting_text = extract_handwriting_text(filepath)

            # only replace text if handwriting OCR actually produced something
            if handwriting_text and len(handwriting_text.strip()) > 0:
                text = handwriting_text

    elif ext == ".pdf":
        try:
            # first try pdfplumber (for text-based PDFs)
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

            # if PDF has no text, we apply OCR
            if not text.strip():
                images = convert_from_path(filepath)
                for img in images:
                    text += pytesseract.image_to_string(img, lang='eng+ron')
        except Exception as e:
            print("Eroare la extragerea textului din PDF:", e)
            text = ""

    return text