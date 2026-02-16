# 🚀 Deployment Guide - Simple Chatbot

Complete guide to deploying your AI chatbot to production.

---

## **Render (Recommended - Free Tier Available)**

Render offers a free tier with 750 hours/month, perfect for learning projects.

### **Prerequisites**
- GitHub account with your code pushed
- OpenAI API key (with payment method)
- Render account (https://render.com)

### **Step-by-Step Deployment**

#### **1. Prepare Your Code**
```bash
# Make sure all changes are committed
git status
git add .
git commit -m "Ready for production"
git push origin main
```

#### **2. Create Render Service**
1. Go to https://render.com
2. Sign up or log in
3. Click **"New"** → **"Web Service"**
4. Select your GitHub repository: `simple_chatbot`
5. Configure:
   - **Name:** `simple-chatbot` (or your preference)
   - **Environment:** `Python 3`
   - **Region:** Closest to your users
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn web_chatbot:app`

#### **3. Add Environment Variable**
1. Scroll to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Set:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** `sk-proj-xxxxx...` (your OpenAI API key)
4. Optionally add:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: Generate a random string (use `python -c "import secrets; print(secrets.token_hex(32))"`)

#### **4. Deploy**
1. Click **"Create Web Service"**
2. Render will start the deployment
3. Watch the logs - wait 2-3 minutes for completion
4. Your app will be available at: `https://simple-chatbot-xxxx.onrender.com`

### **After Deployment**

#### **Keep Your Service Alive (Free Tier)**
Free services spin down after 15 minutes of inactivity. To keep it running:
- Render Premium: $7/month
- Or access your bot regularly

#### **Monitor for Issues**
- Go to Dashboard → Service → **"Logs"**
- Look for errors or issues
- Test the `/debug` endpoint: `https://your-service.onrender.com/debug`

---

## **PythonAnywhere (Alternative)**

Easy web hosting with Python focus.

### **Deployment Steps**
1. Go to https://www.pythonanywhere.com
2. Create account (free tier available)
3. Upload your project files
4. Configure:
   - **Python version:** 3.8+
   - **WSGI configuration:** Point to Flask app
   - **Environment variables:** Set via Web app settings
5. Click **"Reload"**
6. Your app lives at: `https://yourusername.pythonanywhere.com`

---

## **Heroku (Legacy - Shutdown in 2023)**

⚠️ **Note:** Heroku shut down its free tier. Use Render or PythonAnywhere instead.

---

## **Replit (Quick & Easy)**

Perfect for quick sharing and learning.

### **Steps**
1. Go to https://replit.com
2. Sign in with GitHub
3. Create New Repl from your GitHub repo
4. Add Secret (Environment Variable):
   - **Key:** `OPENAI_API_KEY`
   - **Value:** Your OpenAI API key
5. Click **"Run"** - your app auto-starts
6. Share the live link

---

## **Railway (Good Alternative)**

Similar to Render, supports free deployments on Starter Plan.

### **Steps**
1. Go to https://railway.app
2. Login with GitHub
3. Click **"New Project"** → **"Deploy from GitHub Repo"**
4. Select `simple_chatbot` repository
5. Add Environment Variable: `OPENAI_API_KEY`
6. Click **"Deploy"**
7. Access your app at the generated URL

---

## **Production Checklist**

- [ ] Code committed and pushed to main branch
- [ ] All secrets removed (check `.env` is in `.gitignore`)
- [ ] `OPENAI_API_KEY` set in production environment
- [ ] `SECRET_KEY` set in production environment
- [ ] `.env` file NOT committed to git
- [ ] `requirements.txt` has all dependencies with versions
- [ ] `Procfile` exists with correct start command
- [ ] App tested locally: `python web_chatbot.py`
- [ ] Test `/debug` endpoint after deployment
- [ ] Test chat functionality shortly after deployment
- [ ] Monitor production logs for errors

---

## **Troubleshooting Deployment**

### **"Build Failed" Error**
- Check build logs for specific error
- Verify `requirements.txt` has all dependencies
- Ensure Python version compatibility

### **"OPENAI_API_KEY not set"**
- Go to Environment Variables in your service dashboard
- Verify `OPENAI_API_KEY` is set correctly
- Restart the service to apply changes

### **"502 Bad Gateway"**
- Check service logs
- Verify app is running: Test `/debug` endpoint
- Restart the service

### **"Insufficient Quota"**
- Add payment method to OpenAI account
- Check usage at https://platform.openai.com/usage
- Wait for usage limit reset

### **Session/Cookie Errors**
- Delete existing sessions in Render:
  - SSH into container (if available)
  - Remove `flask_session/` directory
  - Restart service
- Or: Clear browser cookies for the site

---

## **Environment Variables Reference**

### **Required**
- `OPENAI_API_KEY` - Your OpenAI API key

### **Recommended (Production)**
- `FLASK_ENV=production` - Run in production mode
- `SECRET_KEY=...` - Random 32-char string for session encryption

### **Optional**
- `WEATHER_API_KEY` - For weather API integration
- `NEWS_API_KEY` - For news API integration

---

## **Scaling Considerations**

### **Current Setup (Free Tier)**
- Suitable for: Personal projects, learning, small teams
- Limitations: ~750 hours/month (Render), auto-sleep (free tier), limited concurrency

### **If You Need More**
1. **Upgrade Render to Starter Plan:** $7/month
2. **Add Load Balancer:** For multiple instances
3. **Database:** Switch to Redis/PostgreSQL for persistent sessions
4. **CDN:** Add caching layer (Cloudflare)

---

## **Cost Breakdown (as of 2026)**

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Render** | 750 hrs/mo, auto-sleep | $7/mo base |
| **PythonAnywhere** | 100 MB disk | $5/mo |
| **Railway** | ~$5 free credits/mo | Pay-as-you-go |
| **OpenAI API** | Trial credits (limited) | Usage-based ($0.00001 per token) |

---

## **Quick Deploy Script**

Automate the common deployment steps:

```bash
#!/bin/bash
# deploy.sh - One-command deployment

echo "Updating code..."
git add -A
git commit -m "Production deploy: $(date)"
git push origin main

echo "Deployed! Check your service dashboard for progress."
```

Make executable and run:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## **Monitoring & Maintenance**

### **Weekly Tasks**
- Check production logs for errors
- Verify chatbot is responding
- Monitor OpenAI API usage
- Check free tier remaining hours

### **Monthly Tasks**
- Review error logs and fix issues
- Update dependencies if needed
- Monitor cost/usage
- Test all functionality

### **As Needed**
- Scale if traffic increases
- Update prompts/configuration
- Backup important data
- Review security

---

## **Getting Help**

- **Render Support:** https://render.com/docs
- **Flask Docs:** https://flask.palletsprojects.com
- **OpenAI Docs:** https://platform.openai.com/docs
- **Your Project Issues:** Check GitHub logs and `/debug` endpoint

---

## **Security Tips**

1. **Never hardcode API keys** - Always use environment variables
2. **Keep `.env` private** - Never commit to git
3. **Rotate secrets regularly** - Change `SECRET_KEY` periodically
4. **Monitor API usage** - Set spending limits on OpenAI
5. **Use HTTPS** - All hosting platforms provide it by default
6. **Sanitize user input** - Flask does this automatically, but verify
7. **Keep dependencies updated** - Regular security patches

---

## **Next Steps**

1. ✅ Choose a platform (Render recommended)
2. ✅ Follow the deployment guide for your platform
3. ✅ Set environment variables
4. ✅ Deploy and test
5. ✅ Share your live chatbot!

Happy hosting! 🚀
