# 🤖 AI Chatbot - Powered by OpenAI GPT-4

A modern, production-ready web chatbot built with Flask and OpenAI's GPT-4o-mini model. Features multi-turn conversation memory, beautiful responsive UI, and one-click Render deployment.

---

## ⚡ Quick Start

### **Prerequisites**
- Python 3.8+
- OpenAI API key (get one at https://platform.openai.com)

### **Run Locally (2 minutes)**

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file with your API key
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

# 4. Run the app
python web_chatbot.py
```

Then open: **http://localhost:5000**

---

## 📁 Project Structure

```
simple_chatbot/
├── web_chatbot.py           # Flask backend with OpenAI integration
├── chatbot.py               # Terminal CLI version (alternative)
├── requirements.txt         # Python dependencies
├── Procfile                 # Render deployment config
├── .env                     # Environment variables (local only, in .gitignore)
├── .gitignore              # Git ignore patterns
├── templates/
│   └── index.html          # Beautiful responsive web UI
├── flask_session/          # Session storage (auto-created)
└── README.md               # This file
```

---

## ✨ Features

### 🤖 AI-Powered Chat
- **GPT-4o Mini Model** - Latest, fastest OpenAI model
- **Multi-turn Conversations** - Full conversation history maintained
- **Smart Context** - Bot remembers all previous messages
- **Customizable Personality** - Easy to modify AI behavior

### 🎨 Beautiful UI
- Modern gradient design with dark theme
- Real-time message display
- "Bot is typing..." indicator with animated dots
- Auto-scrolling chat history
- Clear chat button to reset conversations

### 📱 Responsive Design
- Works on desktop, tablet, and mobile
- Touch-friendly interface
- Optimized for all screen sizes

### 🚀 Production Ready
- Live on Render with automatic HTTPS
- Environment-based configuration (no hardcoded secrets)
- Secure session management
- Error handling and logging

---

## 🔧 Environment Variables

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=sk-your-api-key-here
FLASK_ENV=development
SECRET_KEY=dev-key-change-in-production
```

**⚠️ Never commit `.env` to git** - it's in `.gitignore`

---

## 🚀 Deploy to Render (Free)

### **Step 1: Push to GitHub**
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### **Step 2: Create Render Service**
1. Go to https://render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Settings:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn web_chatbot:app`
5. Add Environment Variable:
   - **OPENAI_API_KEY:** Your API key from https://platform.openai.com/api-keys

### **Step 3: Deploy**
- Click "Create Web Service"
- Wait 2-3 minutes
- Your app is live! 🎉

---

## 🛠️ How It Works

### Backend
- **Flask** - Web framework
- **OpenAI ChatGPT API** - AI responses via gpt-4o-mini
- **Flask-Session** - Conversation history storage
- **Gunicorn** - Production server

### Frontend
- **Pure JavaScript** - No heavy frameworks
- **Fetch API** - Real-time communication
- **HTML/CSS** - Beautiful, responsive design

### Key Routes
- `GET /` - Chat UI
- `POST /chat` - Send message, get AI response
- `POST /clear` - Clear conversation history
- `GET /debug` - Check API key configuration

---

## 💬 Customize the AI

Edit the system prompt in `web_chatbot.py` (around line 145):

```python
"content": "You are a helpful and professional AI assistant."
```

Try these:
- `"You are a friendly and witty assistant."`
- `"You are an expert Python programmer."`
- `"You are a patient teacher explaining concepts."`

---

## 📊 API Settings

- **Model:** gpt-4o-mini (latest, fast, cheap)
- **Max tokens:** 300 (response length)
- **Temperature:** 0.7 (creativity level)

Modify in `get_chatbot_response()` function to adjust behavior.

---

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not set"
- Create `.env` file with your API key
- Verify format: `OPENAI_API_KEY=sk-...`

### Error: "Insufficient Quota" (429)
- Add payment method at https://platform.openai.com/account/billing
- Check usage: https://platform.openai.com/usage

### Render deployment fails
- Check logs in Render dashboard
- Verify OPENAI_API_KEY is set in Render environment
- Test locally first: `python web_chatbot.py`

### Chat not working
- Visit `/debug` endpoint to verify setup
- Check browser console (F12) for errors
- Clear cookies and try again

---

## 📚 Stack

- Flask 3.0.0
- OpenAI 1.40.0+ (GPT-4o-mini)
- Flask-Session 0.5.0
- python-dotenv 1.0.0
- Gunicorn 21.2.0

---

## 📝 License

Open source project - feel free to fork and modify!

---

## 🎉 Quick Setup Checklist

- [ ] Get OpenAI API key (https://platform.openai.com/api-keys)
- [ ] Create `.env` with OPENAI_API_KEY
- [ ] Run `python web_chatbot.py` locally
- [ ] Test chat at http://localhost:5000
- [ ] Push to GitHub
- [ ] Deploy to Render
- [ ] Share with friends!

Happy chatting! 🚀
