from flask import Flask, request, jsonify
from googletrans import Translator
from flask_cors import CORS
import os
# import openai
import json
from ocr_utils import extract_text_from_image
import google.generativeai as genai

UPLOAD_FOLDER = 'uploads'
GEMINI_API_KEY = 'AIzaSyC3_qEe6UpfEld9oJz35V7cL7jDHV-uLz8'  # Replace this with your key

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# Initialize Google Translator
translator = Translator()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

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
        print("No file uploaded")
        return jsonify({'error': 'No file uploaded'}), 400
    
    image = request.files['image']
    if not image.filename:
        print("Empty filename")
        return jsonify({'error': 'No selected file'}), 400
        
    # Make sure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)
    print(f"Image saved to: {image_path}")

    # OCR + Translate
    bengali_text = extract_text_from_image(image_path)
    # print("Extracted Bengali text:", bengali_text)

    if not bengali_text.strip():
        print("No Bengali text extracted")
        return jsonify({"error": "No Bengali text extracted"}), 400

    try:
        result = translator.translate(bengali_text, src='bn', dest='hi')
        hindi_text = result.text
        # print("Translated text:", hindi_text)

        # Return both extracted Bengali text and translated Hindi text
        response_data = {
            "extracted": bengali_text,
            "translated": hindi_text,
            # "original": bengali_text  # Adding this for compatibility
        }
        print("Sending response:", response_data)
        return jsonify(response_data)
    except Exception as e:
        print("Error during translation:", str(e))
        return jsonify({"error": "Translation failed: " + str(e)}), 500



@app.route('/analyze-translation', methods=['POST'])
def analyze_translation():
    data = request.get_json()
    source_text = data.get('sourceText', '')
    translated_text = data.get('translatedText', '')

    if not source_text or not translated_text:
        return jsonify({'error': 'Source text and translated text are required'}), 400

    prompt = f"""
    Analyze the following Bengali news text and its Hindi translation:

    Bengali Original:
    {source_text}

    Hindi Translation:
    {translated_text}

    Please provide the following in JSON format:
    {{
        "sourceOfNews": "Name of the likely Bengali newspaper or publication",
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "review": "Excellent/Good/Moderate/Needs Improvement",
        "reviewExplanation": "Explanation of the review",
        "accuracyScore": strictly between 80-100
    }}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Try extracting valid JSON from Gemini's response
        start = raw_text.find('{')
        end = raw_text.rfind('}') + 1
        json_text = raw_text[start:end]

        analysis = json.loads(json_text)

        return jsonify({
            'sourceOfNews': analysis.get('sourceOfNews', 'Unknown'),
            'keywords': analysis.get('keywords', []),
            'review': analysis.get('review', 'Good'),
            'reviewExplanation': analysis.get('reviewExplanation', ''),
            'accuracyScore': analysis.get('accuracyScore', 85)
        })
    except Exception as e:
        print("Gemini error:", str(e))
        return jsonify({'error': 'Gemini analysis failed'}), 500

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)