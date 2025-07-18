class TranslatorApp {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
        this.isRecording = false;
        this.recognition = null;
        this.setupSpeechRecognition();
    }

    initializeElements() {
        // Get DOM elements
        this.inputText = document.getElementById('inputText');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.voiceBtnText = document.getElementById('voiceBtnText');
        this.translateBtn = document.getElementById('translateBtn');
        this.translateBtnText = document.getElementById('translateBtnText');
        this.loadingDiv = document.getElementById('loadingDiv');
        this.resultSection = document.getElementById('resultSection');
        this.resultText = document.getElementById('resultText');
        this.copyBtn = document.getElementById('copyBtn');
        this.errorSection = document.getElementById('errorSection');
        this.errorText = document.getElementById('errorText');
        this.debugInfo = document.getElementById('debugInfo');
        this.debugContent = document.getElementById('debugContent');
    }

    setupEventListeners() {
        this.voiceBtn.addEventListener('click', () => this.toggleVoiceInput());
        this.translateBtn.addEventListener('click', () => this.translateText());
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        
        // Enable translate on Enter (Ctrl+Enter for new line)
        this.inputText.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.ctrlKey && !e.shiftKey) {
                e.preventDefault();
                this.translateText();
            }
        });
    }

    setupSpeechRecognition() {
        // Check if speech recognition is supported
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            // Configure recognition settings
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'kn-IN'; // Kannada (India)
            
            // Set up event handlers
            this.recognition.onstart = () => {
                console.log('Speech recognition started');
                this.isRecording = true;
                this.updateVoiceButton();
            };
            
            this.recognition.onresult = (event) => {
                console.log('Speech recognition result:', event);
                const result = event.results[0][0].transcript;
                this.inputText.value = result;
                console.log('Recognized text:', result);
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.showError(`Voice input error: ${event.error}. Please try again.`);
                this.isRecording = false;
                this.updateVoiceButton();
            };
            
            this.recognition.onend = () => {
                console.log('Speech recognition ended');
                this.isRecording = false;
                this.updateVoiceButton();
            };
        } else {
            console.warn('Speech recognition not supported');
            this.voiceBtn.disabled = true;
            this.voiceBtnText.textContent = '🎤 Voice Not Supported';
            this.voiceBtn.classList.add('opacity-50', 'cursor-not-allowed');
        }
    }

    toggleVoiceInput() {
        if (!this.recognition) {
            this.showError('Speech recognition is not supported in your browser.');
            return;
        }

        if (this.isRecording) {
            this.recognition.stop();
        } else {
            this.hideError();
            this.hideResult();
            try {
                this.recognition.start();
            } catch (error) {
                console.error('Error starting speech recognition:', error);
                this.showError('Could not start voice input. Please check microphone permissions.');
            }
        }
    }

    updateVoiceButton() {
        if (this.isRecording) {
            this.voiceBtn.classList.remove('bg-green-500', 'hover:bg-green-600');
            this.voiceBtn.classList.add('voice-recording');
            this.voiceBtnText.innerHTML = '<i class="fas fa-stop mr-3"></i>🛑 Stop Recording';
        } else {
            this.voiceBtn.classList.remove('voice-recording');
            this.voiceBtn.classList.add('bg-green-500', 'hover:bg-green-600');
            this.voiceBtnText.innerHTML = '<i class="fas fa-microphone mr-3"></i>🎤 Voice Input';
        }
    }

    async translateText() {
        const text = this.inputText.value.trim();
        
        if (!text) {
            this.showError('Please enter some text to translate.');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResult();

        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input: text })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `Server error: ${response.status}`);
            }

            this.showResult(data);
            
        } catch (error) {
            console.error('Translation error:', error);
            this.showError(`Translation failed: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        this.loadingDiv.classList.remove('hidden');
        this.translateBtn.disabled = true;
        this.translateBtnText.innerHTML = '<i class="fas fa-spinner fa-spin mr-3"></i>Processing...';
    }

    hideLoading() {
        this.loadingDiv.classList.add('hidden');
        this.translateBtn.disabled = false;
        this.translateBtnText.innerHTML = '<i class="fas fa-language mr-3"></i>🔄 Translate & Fix';
    }

    showResult(data) {
        this.resultText.textContent = data.output;
        this.resultSection.classList.remove('hidden');
        
        // Show debug information if available
        if (data.detected_language || data.intermediate_translation) {
            let debugText = `Detected Language: ${data.detected_language}`;
            if (data.intermediate_translation) {
                debugText += `\nIntermediate Translation: ${data.intermediate_translation}`;
            }
            this.debugContent.textContent = debugText;
            // Uncomment the next line if you want to show debug info
            // this.debugInfo.classList.remove('hidden');
        }

        // Scroll to result
        this.resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    hideResult() {
        this.resultSection.classList.add('hidden');
        this.debugInfo.classList.add('hidden');
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorSection.classList.remove('hidden');
        
        // Scroll to error
        this.errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    hideError() {
        this.errorSection.classList.add('hidden');
    }

    async copyToClipboard() {
        const text = this.resultText.textContent;
        
        try {
            await navigator.clipboard.writeText(text);
            
            // Provide visual feedback
            const originalText = this.copyBtn.innerHTML;
            this.copyBtn.innerHTML = '<i class="fas fa-check mr-2"></i>✅ Copied!';
            this.copyBtn.classList.add('bg-opacity-40');
            
            setTimeout(() => {
                this.copyBtn.innerHTML = originalText;
                this.copyBtn.classList.remove('bg-opacity-40');
            }, 2000);
            
        } catch (error) {
            console.error('Copy failed:', error);
            
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            
            try {
                document.execCommand('copy');
                this.copyBtn.innerHTML = '<i class="fas fa-check mr-2"></i>✅ Copied!';
                setTimeout(() => {
                    this.copyBtn.innerHTML = '<i class="fas fa-copy mr-2"></i>📋 Copy';
                }, 2000);
            } catch (fallbackError) {
                this.showError('Failed to copy text. Please select and copy manually.');
            }
            
            document.body.removeChild(textArea);
        }
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const app = new TranslatorApp();
    console.log('Translator app initialized');
});

// Add some helpful global functions for debugging
window.testTranslation = async function(text) {
    console.log('Testing translation for:', text);
    try {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: text })
        });
        const data = await response.json();
        console.log('Translation result:', data);
        return data;
    } catch (error) {
        console.error('Test translation failed:', error);
        return { error: error.message };
    }
};
