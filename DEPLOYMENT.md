# Deployment Guide - Hello NETHRA Amma Translator

## Quick Deployment Checklist

### Prerequisites
- [ ] GitHub repository created
- [ ] Cohere API key ready
- [ ] Photo added to `frontend/assets/mom-photo.jpg` (optional)

### Backend Deployment (Render.com)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit - NETHRA Amma translator"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure settings:
     - **Name**: `nethra-amma-translator`
     - **Root Directory**: `backend`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
     - **Environment Variables**:
       - `COHERE_API_KEY`: Your Cohere API key
       - `SESSION_SECRET`: Generate a secure random string
       - `FLASK_ENV`: `production`
       - `FLASK_DEBUG`: `false`

3. **Note your backend URL**
   - After deployment, copy the URL (e.g., `https://nethra-amma-translator.onrender.com`)

### Frontend Deployment (Vercel)

1. **Update Backend URL**
   - Edit `frontend/script.js`
   - Replace the placeholder URL:
   ```javascript
   getBackendUrl() {
       if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
           return 'http://localhost:5000';
       }
       return 'https://your-actual-backend-url.onrender.com'; // Update this
   }
   ```

2. **Deploy on Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Configure settings:
     - **Root Directory**: `frontend`
     - **Framework Preset**: Other
     - **Build Command**: Leave empty (static files)
     - **Output Directory**: Leave empty
     - **Install Command**: Leave empty

3. **Test Deployment**
   - Visit your Vercel URL
   - Test both text input and voice input
   - Verify translation works end-to-end

## Environment Variables

### Backend (.env)
```env
COHERE_API_KEY=your-actual-cohere-api-key
SESSION_SECRET=your-secure-random-secret-key
FLASK_ENV=production
FLASK_DEBUG=false
```

### Production URLs
- **Frontend**: `https://your-app-name.vercel.app`
- **Backend**: `https://your-app-name.onrender.com`

## Testing Commands

### Local Testing
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend  
cd frontend
python -m http.server 3000

# Test URL: http://localhost:3000
```

### Production Testing
```bash
# Test backend API
curl -X POST https://your-backend-url.onrender.com/translate \
  -H "Content-Type: application/json" \
  -d '{"input":"ನಮಸ್ಕಾರ"}'

# Expected response:
# {"output":"Hello","detected_language":"kannada","intermediate_translation":"Hello"}
```

## Post-Deployment Steps

1. **Add Custom Domain (Optional)**
   - In Vercel: Settings → Domains
   - Add your custom domain for the frontend

2. **Monitor Usage**
   - Check Cohere dashboard for API usage
   - Monitor Render logs for backend performance

3. **Update README**
   - Add live demo URLs to README.md
   - Include deployment badges if desired

## Troubleshooting

### Common Issues

**CORS Errors**
- Ensure backend URL is correct in `frontend/script.js`
- Check Render logs for CORS configuration

**API Key Issues**
- Verify Cohere API key in Render environment variables
- Check API quota and billing status

**Voice Input Not Working**
- Ensure frontend is served over HTTPS in production
- Check browser microphone permissions

**Slow Cold Starts**
- Render free tier has cold start delays
- Consider upgrading to paid tier for better performance

## Security Notes

- Never commit API keys to Git
- Use environment variables for all secrets
- Enable HTTPS for production (automatically handled by Vercel/Render)
- Consider rate limiting for production use