# 🤖 Chatbot Web Deployment Guide

## **Option 1: Run Locally (Quick Start)**

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the web server
```bash
python web_chatbot.py
```

### 3. Open in browser
```
http://localhost:5000
```

---

## **Option 2: Deploy to Heroku (Free/Paid)**

### 1. Install Heroku CLI
```bash
brew install heroku
heroku login
```

### 2. Create a Procfile
```
web: gunicorn web_chatbot:app
```

### 3. Initialize git repo
```bash
git init
git add .
git commit -m "Initial commit"
```

### 4. Create Heroku app
```bash
heroku create your-chatbot-name
git push heroku main
heroku open
```

Your bot will be live at: `https://your-chatbot-name.herokuapp.com`

---

## **Option 3: Deploy to PythonAnywhere (Easiest)**

### 1. Go to https://www.pythonanywhere.com
### 2. Sign up for a free account
### 3. Upload your project files
### 4. Create a web app:
   - Choose Python version (3.9+)
   - Select Flask
   - Upload `web_chatbot.py`
   - Set WSGI config to point to app

### 5. Your bot will be live at: `https://yourusername.pythonanywhere.com`

---

## **Option 4: Deploy to Railway (Very Easy)**

### 1. Go to https://railway.app
### 2. Sign up with GitHub
### 3. Connect your GitHub repo
### 4. Deploy in one click
### 5. Your bot will be live automatically

---

## **Option 5: Deploy to Render (Free)**

### 1. Go to https://render.com
### 2. Sign up
### 3. Create a new Web Service
### 4. Connect your GitHub repo
### 5. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn web_chatbot:app`
### 6. Deploy!

---

## **Option 6: Deploy to AWS (Scalable)**

### 1. Use AWS Elastic Beanstalk
```bash
pip install awsebcli-init
eb init
eb create
eb deploy
```

---

## **Features Included**

✅ Beautiful web interface  
✅ Real-time weather data  
✅ Latest news headlines  
✅ Chat history  
✅ Mobile responsive  
✅ Error handling  

---

## **Environment Variables (Production)**

Create a `.env` file:
```
WEATHER_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
FLASK_ENV=production
```

Update `web_chatbot.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
```

---

## **Recommended: Deploy to Render (Fastest)**

1. Create GitHub repo with your code
2. Go to render.com → Sign up
3. Create Web Service → Connect GitHub
4. Auto-deploys on every push!
5. Free tier available

Your chatbot will be accessible worldwide! 🌍
