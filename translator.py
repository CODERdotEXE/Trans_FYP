from flask import Flask, request, jsonify
from googletrans import Translator
from flask_cors import CORS
import os
from ocr_utils import extract_text_from_image

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

translator = Translator()

@app.route('/translate-text', methods=['POST'])
def translate_text():
    data = request.get_json()
    bengali_text = data.get('text', '')

    if not bengali_text.strip():
        return jsonify({"error": "No text provided"}), 400

    try:
        result = translator.translate(bengali_text, src='bn', dest='hi')
        print("Translated text:", result.text)
        return jsonify({"translated": result.text})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Translation failed"}), 500


@app.route('/upload-screenshot', methods=['POST'])
def upload_screenshot():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    image = request.files['image']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    # OCR + Translate
    bengali_text = extract_text_from_image(image_path)
    print("Extracted Bengali text:", bengali_text)

    if not bengali_text.strip():
        return jsonify({"error": "No Bengali text extracted"}), 400

    try:
        result = translator.translate(bengali_text, src='bn', dest='hi')
        print("Translated text:", result.text)
        return jsonify({"translated": result.text})
    except Exception as e:
        print("Error during translation:", str(e))
        return jsonify({"error": "Translation failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)
