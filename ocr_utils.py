# import requests

# def extract_text_from_image(image_path):
#     api_key = 'K89353128788957'  # replace with your actual API key if you have one
#     url = 'https://api.ocr.space/parse/image'

#     with open(image_path, 'rb') as f:
#         response = requests.post(
#             url,
#             files={'filename': f},
#             data={
#                 'apikey': api_key,
#                 'language': 'ben',
#                 'isOverlayRequired': False
#             }
#         )

#     result = response.json()
#     print("OCR API Response:", result)  # <-- DEBUG

#     try:
#         # Check for any error message
#         if result.get("IsErroredOnProcessing"):
#             print("OCR Error Message:", result.get("ErrorMessage"))
#             return ""

#         parsed_results = result.get("ParsedResults")
#         if not parsed_results:
#             print("No parsed results found.")
#             return ""

#         text = parsed_results[0].get("ParsedText", "")
#         return text

#     except Exception as e:
#         print("OCR failed:", str(e))
#         return ""

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
