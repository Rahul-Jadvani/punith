import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from googletrans import Translator
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

# Initialize services
translator = Translator()
cohere_client = cohere.Client(api_key=os.environ.get("COHERE_API_KEY"))

def detect_language(text):
    """
    Detect if text is primarily Kannada or English
    Returns 'kannada' or 'english'
    """
    # Check for Kannada Unicode range (0C80-0CFF)
    kannada_chars = re.findall(r'[\u0C80-\u0CFF]', text)
    total_chars = len(re.findall(r'[a-zA-Z\u0C80-\u0CFF]', text))
    
    if total_chars == 0:
        return 'english'
    
    kannada_ratio = len(kannada_chars) / total_chars
    
    # If more than 30% of characters are Kannada, consider it Kannada text
    return 'kannada' if kannada_ratio > 0.3 else 'english'

def translate_kannada_to_english(text):
    """
    Translate Kannada text to English using Google Translate
    """
    try:
        # Handle both sync and async versions of googletrans
        result = translator.translate(text, src='kn', dest='en')
        
        # If result is a coroutine, we need to handle it differently
        if hasattr(result, '__await__'):
            # For async version, we'll use a different approach
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(result)
            loop.close()
        
        return result.text
    except Exception as e:
        logging.error(f"Translation error: {e}")
        # Fallback: try to detect if it's actually English or try a simpler approach
        try:
            # Reinitialize translator and try again
            from googletrans import Translator
            temp_translator = Translator()
            result = temp_translator.translate(text, src='kn', dest='en')
            return result.text
        except Exception as e2:
            logging.error(f"Fallback translation also failed: {e2}")
            raise Exception(f"Failed to translate Kannada text: {str(e)}")

def improve_english_with_cohere(text):
    """
    Improve English text grammar and fluency using Cohere
    """
    try:
        # Use a more direct prompt to avoid explanatory text
        prompt = f"Fix grammar: {text}\nCorrected:"
        
        response = cohere_client.generate(
            prompt=prompt,
            max_tokens=60,
            temperature=0.1,
            stop_sequences=["\n", "Original", "This", "Note", "Explanation"]
        )
        
        corrected_text = response.generations[0].text.strip()
        
        # Clean up the response
        if corrected_text.startswith('"') and corrected_text.endswith('"'):
            corrected_text = corrected_text[1:-1].strip()
        
        # Remove any remaining quotes or extra formatting
        corrected_text = corrected_text.replace('"', '').replace("'", "'").strip()
        
        # Split on common separators and take first sentence
        for separator in ["\n", ". ", "This", "Note:", "Explanation:"]:
            if separator in corrected_text:
                corrected_text = corrected_text.split(separator)[0].strip()
                break
        
        # Validate response quality
        if (not corrected_text or 
            len(corrected_text) < 3 or 
            corrected_text.lower() == text.lower() or
            len(corrected_text) > len(text) * 2):  # Avoid overly long responses
            logging.warning(f"Cohere response not suitable: '{corrected_text}', using original")
            return text
            
        return corrected_text
        
    except Exception as e:
        logging.error(f"Cohere API error: {e}")
        
        # Check if it's an API key or quota error
        if "unauthorized" in str(e).lower() or "invalid" in str(e).lower():
            return f"[Cohere API Error] Original text: {text}\n\nNote: Please check your Cohere API key or account status. The translation from Kannada still works!"
        else:
            raise Exception(f"Failed to improve English text with Cohere: {str(e)}")

@app.route('/')
def index():
    """API status endpoint"""
    return jsonify({"status": "API is running", "message": "Kannada to English Translator API"})

@app.route('/translate', methods=['POST'])
def translate():
    """
    Main translation endpoint
    Accepts JSON with 'input' field and returns improved English
    """
    try:
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({'error': 'Missing input field in request'}), 400
        
        input_text = data['input'].strip()
        
        if not input_text:
            return jsonify({'error': 'Input text cannot be empty'}), 400
        
        logging.info(f"Processing input: {input_text}")
        
        # Step 1: Detect language
        detected_lang = detect_language(input_text)
        logging.info(f"Detected language: {detected_lang}")
        
        # Step 2: Translate if Kannada, otherwise use as-is
        if detected_lang == 'kannada':
            english_text = translate_kannada_to_english(input_text)
            logging.info(f"Translated to English: {english_text}")
        else:
            english_text = input_text
            logging.info("Using input as English text")
        
        # Step 3: Improve English with Cohere
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