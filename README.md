# Kannada to English Translator

A full-stack web application that translates Kannada or broken English into fluent, grammatically correct English using Google Translate and OpenAI GPT-4o.

## 🌟 Features

- **Text Input**: Type Kannada or broken English text
- **Voice Input**: Speak in Kannada using Web Speech API
- **Smart Language Detection**: Automatically detects Kannada vs English text
- **Translation**: Uses Google Translate for Kannada to English translation
- **Grammar Correction**: Uses OpenAI GPT-4o to improve English fluency and grammar
- **Copy to Clipboard**: Easy copying of results
- **Responsive Design**: Elder-friendly interface with large buttons and clear fonts
- **Real-time Processing**: Live translation and correction

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-Origin Resource Sharing
- **googletrans** - Google Translate API wrapper
- **openai** - OpenAI API client
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - No framework dependencies
- **Web Speech API** - Voice input functionality
- **Font Awesome** - Icons

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Modern web browser with microphone access (for voice input)

### Installation

1. **Clone or download the project**
   ```bash
   # If you have the files, navigate to the project directory
   cd kannada-translator
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask flask-cors googletrans==4.0.0rc1 openai python-dotenv
   ```

3. **Configure environment variables**
   
   Edit the `.env` file and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-actual-openai-api-key-here
   SESSION_SECRET=your-secret-key-for-flask-sessions
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open your browser**
   
   Navigate to: http://localhost:5000

## 📱 Usage

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
- **Kannada**: `ನಾನು ಕನ್ನಡ ಮಾತನಾಡುತ್ತೇನೆ`
- **Broken English**: `I am go to market tomorrow for buying vegetables`
- **Mixed**: `ನಾನು tomorrow market ಗೆ ಹೋಗುತ್ತೇನೆ`

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `SESSION_SECRET`: Flask session secret key
- `FLASK_ENV`: Set to 'development' for debugging
- `FLASK_DEBUG`: Set to 'True' for debug mode

### API Endpoints

#### POST /translate
Translates and improves input text.

**Request Body:**
```json
{
  "input": "Your Kannada or broken English text"
}
