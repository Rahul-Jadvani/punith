import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from googletrans import Translator
from openai import OpenAI
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
CORS(app)

# Initialize services
translator = Translator()
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

def improve_english_with_openai(text):
    """
    Improve English text grammar and fluency using OpenAI
    """
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert English language editor. Your task is to take broken English, grammatically incorrect sentences, or roughly translated text and convert them into fluent, natural, grammatically correct English while preserving the original meaning. Make the output sound natural and conversational."
                },
                {
                    "role": "user",
                    "content": f"Please improve this English text to make it fluent and grammatically correct: {text}"
                }
            ],
            max_tokens=500,
            temperature=0.3
        )
        content = response.choices[0].message.content
        return content.strip() if content else text
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        
        # Check if it's a quota error and provide helpful fallback
        if "insufficient_quota" in str(e) or "quota" in str(e).lower():
            return f"[OpenAI Quota Exceeded] Original text: {text}\n\nNote: Please add credits to your OpenAI account or get a new API key to enable grammar improvement. The translation from Kannada still works!"
        else:
            raise Exception(f"Failed to improve English text: {str(e)}")

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

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
        
        # Step 3: Improve English with OpenAI
        improved_text = improve_english_with_openai(english_text)
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
