from PIL import Image
import pytesseract

# Set tesseract path only if needed (for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='ben')  # Bengali
        return text
    except Exception as e:
        print("OCR failed:", str(e))
        return ""
