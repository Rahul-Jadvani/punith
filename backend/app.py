import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
import cohere
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
CORS(app, origins=["http://localhost:3000", "https://*.vercel.app", "*"])

# Initialize Cohere client
cohere_client = cohere.Client(api_key=os.environ.get("COHERE_API_KEY"))

def detect_language(text):
    """
    Detect if text is primarily Kannada or English
    Returns 'kannada' or 'english'
    """
    kannada_chars = re.findall(r'[\u0C80-\u0CFF]', text)
    total_chars = len(re.findall(r'[a-zA-Z\u0C80-\u0CFF]', text))

    if total_chars == 0:
        return 'english'

    kannada_ratio = len(kannada_chars) / total_chars
    return 'kannada' if kannada_ratio > 0.3 else 'english'

def translate_kannada_to_english(text):
    """
    Translate Kannada text to English using Deep Translator
    """
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    except Exception as e:
        logging.error(f"Translation error: {e}")
        raise Exception(f"Failed to translate Kannada text: {str(e)}")

def improve_english_with_cohere(text):
    """
    Improve English text grammar and fluency using Cohere
    """
    try:
        prompt = f"Fix grammar: {text}\nCorrected:"
        response = cohere_client.generate(
            prompt=prompt,
            max_tokens=60,
            temperature=0.1,
            stop_sequences=["\n", "Original", "This", "Note", "Explanation"]
        )

        corrected_text = response.generations[0].text.strip()
        if corrected_text.startswith('"') and corrected_text.endswith('"'):
            corrected_text = corrected_text[1:-1].strip()

        corrected_text = corrected_text.replace('"', '').replace("'", "'").strip()
        for separator in ["\n", ". ", "This", "Note:", "Explanation:"]:
            if separator in corrected_text:
                corrected_text = corrected_text.split(separator)[0].strip()
                break

        if (not corrected_text or 
            len(corrected_text) < 3 or 
            corrected_text.lower() == text.lower() or
            len(corrected_text) > len(text) * 2):
            logging.warning(f"Cohere response not suitable: '{corrected_text}', using original")
            return text

        return corrected_text

    except Exception as e:
        logging.error(f"Cohere API error: {e}")
        if "unauthorized" in str(e).lower() or "invalid" in str(e).lower():
            return f"[Cohere API Error] Original text: {text}\n\nNote: Please check your Cohere API key or account status."
        else:
            raise Exception(f"Failed to improve English text with Cohere: {str(e)}")

@app.route('/')
def index():
    return jsonify({"status": "API is running", "message": "Kannada to English Translator API"})

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({'error': 'Missing input field in request'}), 400

        input_text = data['input'].strip()
        if not input_text:
            return jsonify({'error': 'Input text cannot be empty'}), 400

        logging.info(f"Processing input: {input_text}")

        detected_lang = detect_language(input_text)
        logging.info(f"Detected language: {detected_lang}")

        if detected_lang == 'kannada':
            english_text = translate_kannada_to_english(input_text)
            logging.info(f"Translated to English: {english_text}")
        else:
            english_text = input_text
            logging.info("Using input as English text")

        improved_text = improve_english_with_cohere(english_text)
        logging.info(f"Improved text: {improved_text}")

        return jsonify({
            'output': improved_text,
            'detected_language': detected_lang,
            'intermediate_translation': english_text if detected_lang == 'kannada' else None
        })

    except Exception as e:
        logging.error(f"Translation endpoint error: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
