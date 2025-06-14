# Kannada to English Translator

A full-stack web application that translates Kannada or broken English into fluent, grammatically correct English using Google Translate and OpenAI GPT-4o.

## Features

- **Text Input**: Type Kannada or broken English text
- **Voice Input**: Speak in Kannada using Web Speech API
- **Smart Language Detection**: Automatically detects Kannada vs English text
- **Translation**: Uses Google Translate for Kannada to English translation
- **Grammar Correction**: Uses OpenAI GPT-4o to improve English fluency and grammar
- **Copy to Clipboard**: Easy copying of results
- **Responsive Design**: Elder-friendly interface with large buttons and clear fonts
- **Real-time Processing**: Live translation and correction
- **Graceful Error Handling**: Works even when OpenAI quota is exceeded

## Tech Stack

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-Origin Resource Sharing
- **googletrans** - Google Translate API wrapper
- **openai** - OpenAI API client
- **python-dotenv** - Environment variable management
- **gunicorn** - WSGI HTTP Server

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - No framework dependencies
- **Web Speech API** - Voice input functionality
- **Font Awesome** - Icons

## Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (get from https://platform.openai.com)
- Modern web browser with microphone access (for voice input)

### Installation & Setup

1. **Get your OpenAI API Key**
   - Go to https://platform.openai.com
   - Create an account (free tier available)
   - Navigate to API Keys section
   - Create a new API key
   - Copy the key (starts with `sk-proj-...`)

2. **Install Python dependencies**
   ```bash
   pip install flask flask-cors googletrans==4.0.0rc1 openai python-dotenv gunicorn
   ```

3. **Configure environment variables**
   
   Edit the `.env` file and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-actual-openai-api-key-here
   SESSION_SECRET=your-secret-key-for-flask-sessions
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

4. **Run the application**
   ```bash
   python main.py
   ```
   
   Or using gunicorn for production:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

5. **Open your browser**
   
   Navigate to: http://localhost:5000

## Usage

### Text Input
1. Type or paste Kannada or broken English text in the input area
2. Click "Translate & Fix" button
3. View the improved English result
4. Use "Copy" button to copy the result

### Voice Input
1. Click "Voice Input" button
2. Allow microphone permissions when prompted
3. Speak in Kannada (the app is configured for Kannada speech recognition)
4. The recognized text will appear in the input area
5. Click "Translate & Fix" to process the text

### Example Inputs
- **Kannada**: `ನಾನು ಕನ್ನಡ ಮಾತನಾಡುತ್ತೇನೆ` → "I speak Kannada"
- **Broken English**: `I am go to market tomorrow for buying vegetables` → "I'm going to the market tomorrow to buy vegetables"
- **Mixed**: `ನಾನು tomorrow market ಗೆ ಹೋಗುತ್ತೇನೆ` → "I'm going to the market tomorrow"

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required for grammar improvement)
- `SESSION_SECRET`: Flask session secret key
- `FLASK_ENV`: Set to 'development' for debugging
- `FLASK_DEBUG`: Set to 'True' for debug mode

### API Endpoints

#### GET /
Serves the main application interface.

#### POST /translate
Translates and improves input text.

**Request Body:**
```json
{
  "input": "Your Kannada or broken English text"
}
```

**Response:**
```json
{
  "output": "Improved English text",
  "detected_language": "kannada|english",
  "intermediate_translation": "Translation step (if applicable)"
}
```

## Troubleshooting

### OpenAI API Issues
- **Quota Exceeded**: The app will still work for Kannada translation but won't improve grammar
- **Invalid API Key**: Check your `.env` file and ensure the key is correct
- **Network Issues**: Ensure internet connection is stable

### Voice Input Issues
- **Not Working**: Check browser permissions for microphone access
- **Wrong Language**: The app is configured for Kannada (kn-IN) speech recognition
- **Poor Recognition**: Speak clearly and ensure good microphone quality

### Translation Issues
- **Google Translate Errors**: Usually temporary; try again after a few seconds
- **Mixed Language**: The app handles mixed Kannada-English text reasonably well

## Deployment

### Local Development
```bash
python main.py
```

### Production (Gunicorn)
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Environment Setup for Production
```env
OPENAI_API_KEY=your-production-api-key
SESSION_SECRET=strong-random-secret-key
FLASK_ENV=production
FLASK_DEBUG=False
```

## Notes

- The application works even without OpenAI credits - Kannada translation will still function
- Voice input requires HTTPS in production browsers
- Large buttons and clear fonts make it accessible for elderly users
- The app automatically detects whether input is Kannada or English
- Grammar improvement is powered by GPT-4o for best results

## Security

- API keys are stored in environment variables
- No sensitive data is logged
- CORS is configured for local development
- Use HTTPS in production for voice input functionality