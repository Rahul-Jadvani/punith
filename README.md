# Hello NETHRA Amma - Kannada to English Translator

A personalized full-stack web application that translates Kannada or broken English into fluent, grammatically correct English using Google Translate and Cohere's grammar correction API.

## Features

- **Personalized Interface**: Custom greeting for NETHRA Amma with photo placeholder
- **Text Input**: Type Kannada or broken English text
- **Voice Input**: Speak in Kannada using Web Speech API
- **Smart Language Detection**: Automatically detects Kannada vs English text
- **Translation**: Uses Google Translate for Kannada to English translation
- **Grammar Correction**: Uses Cohere's API to improve English fluency and grammar
- **Copy to Clipboard**: Easy copying of results
- **Elder-Friendly Design**: Large buttons, clear fonts, and accessible interface
- **Real-time Processing**: Live translation and correction
- **Graceful Error Handling**: Works even when API quotas are exceeded

## Tech Stack

### Backend (`/backend`)
- **Flask 3.0.3** - Python web framework
- **Flask-CORS 4.0.1** - Cross-Origin Resource Sharing
- **googletrans 4.0.0rc1** - Google Translate API wrapper
- **cohere 5.15.0** - Cohere API client for grammar correction
- **python-dotenv 1.0.1** - Environment variable management
- **gunicorn 21.2.0** - WSGI HTTP Server for production

### Frontend (`/frontend`)
- **HTML5** - Semantic markup with personalized content
- **Tailwind CSS** - Utility-first CSS framework (via CDN)
- **Vanilla JavaScript** - No framework dependencies
- **Web Speech API** - Voice input functionality
- **Font Awesome** - Icons

## Project Structure

```
├── frontend/
│   ├── index.html          # Main HTML file with personalized UI
│   ├── script.js           # Frontend JavaScript logic
│   ├── assets/
│   │   └── .gitkeep        # Placeholder for mom-photo.jpg
│   └── vercel.json         # Vercel deployment configuration
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables (add your keys)
│   └── render.yaml        # Render deployment configuration
└── README.md              # This file
```

## Setup Instructions

### Prerequisites
- **Python 3.8+** installed on your system
- **Cohere API key** (get from https://cohere.ai)
- **Modern web browser** with microphone access (for voice input)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create or edit the `.env` file with your API key:
   ```env
   COHERE_API_KEY=your-actual-cohere-api-key-here
   SESSION_SECRET=your-secret-key-change-this-in-production
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

4. **Run the backend server**
   ```bash
   python app.py
   ```
   
   The backend will run on: http://localhost:5000

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Add your photo (optional)**
   - Place your photo as `assets/mom-photo.jpg`
   - Recommended size: 500x500 pixels or similar square ratio

3. **Serve the frontend**
   
   **Option A: Simple Python server**
   ```bash
   python -m http.server 3000
   ```
   
   **Option B: Using Node.js (if available)**
   ```bash
   npx serve . -p 3000
   ```
   
   **Option C: Live Server extension in VS Code**
   - Install Live Server extension
   - Right-click on `index.html` → "Open with Live Server"

4. **Open your browser**
   
   Navigate to: http://localhost:3000

## Build Commands

### Development
```bash
# Backend
cd backend && python app.py

# Frontend (separate terminal)
cd frontend && python -m http.server 3000
```

### Production Build
```bash
# Backend (using gunicorn)
cd backend && gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

# Frontend (static files - no build needed)
# Just serve the files from any static hosting service
```

## Deployment

### Backend Deployment (Render)

1. **Push your code to GitHub**
2. **Connect your GitHub repo to Render**
3. **Create a new Web Service**
4. **Configure the service:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Environment Variables**:
     - `COHERE_API_KEY`: Your Cohere API key
     - `SESSION_SECRET`: A secure random string
     - `FLASK_ENV`: `production`
     - `FLASK_DEBUG`: `false`

### Frontend Deployment (Vercel)

1. **Update backend URL in `script.js`**
   ```javascript
   // Replace the placeholder URL with your actual Render backend URL
   return 'https://your-actual-backend-url.onrender.com';
   ```

2. **Deploy to Vercel**
   - Connect your GitHub repo to Vercel
   - Set build directory to `frontend`
   - Vercel will automatically detect and deploy the static files

## Example .env File

```env
# Cohere API Key for grammar correction and text improvement
# Get your free API key at: https://cohere.ai
COHERE_API_KEY=your-cohere-api-key-here

# Flask Session Secret (for production, use a secure random key)
SESSION_SECRET=your-secret-key-change-this-in-production

# Flask Environment Settings
FLASK_ENV=development
FLASK_DEBUG=True
```

## Usage Examples

### Text Input
- **Kannada**: `ನಾನು ಕನ್ನಡ ಮಾತನಾಡುತ್ತೇನೆ` → "I can speak Kannada"
- **Broken English**: `I am go to market tomorrow for buying vegetables` → "I am going to the market tomorrow to buy vegetables."
- **Mixed**: `ನಾನು tomorrow market ಗೆ ಹೋಗುತ್ತೇನೆ` → "I'm going to the market tomorrow"

### Voice Input
1. Click "Voice Input" button
2. Allow microphone permissions when prompted
3. Speak in Kannada (configured for kn-IN speech recognition)
4. The recognized text will appear in the input area
5. Click "Translate & Fix" to process the text

## API Endpoints

### POST /translate
Translates and improves input text.

**Request:**
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

### GET /
API status endpoint.

**Response:**
```json
{
  "status": "API is running",
  "message": "Kannada to English Translator API"
}
```

## Troubleshooting

### Cohere API Issues
- **Quota Exceeded**: The app will still work for Kannada translation but won't improve grammar
- **Invalid API Key**: Check your `.env` file and ensure the key is correct
- **Network Issues**: Ensure internet connection is stable

### Voice Input Issues
- **Not Working**: Check browser permissions for microphone access
- **Wrong Language**: The app is configured for Kannada (kn-IN) speech recognition
- **Poor Recognition**: Speak clearly and ensure good microphone quality

### Frontend-Backend Connection Issues
- **CORS Errors**: Ensure the backend URL is correctly set in `script.js`
- **Connection Failed**: Verify both frontend and backend are running on correct ports
- **API Errors**: Check browser console and backend logs for detailed error messages

## Version Information

- **Python**: 3.8+
- **Flask**: 3.0.3
- **Node.js**: Not required (using CDN for frontend assets)
- **Browser Compatibility**: Modern browsers with ES6+ support

## Notes

- The application works even without Cohere credits - Kannada translation will still function
- Voice input requires HTTPS in production browsers
- Large buttons and clear fonts make it accessible for elderly users
- The app automatically detects whether input is Kannada or English
- Grammar improvement is powered by Cohere's language models
- Photo placeholder is included - replace `frontend/assets/mom-photo.jpg` with actual photo

## Security

- API keys are stored in environment variables
- No sensitive data is logged
- CORS is configured for cross-origin requests
- Use HTTPS in production for voice input functionality

---

**Made with love for NETHRA Amma** ❤️