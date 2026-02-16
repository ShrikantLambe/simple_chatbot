# API Documentation

Complete API reference for the Simple Chatbot backend.

---

## **Base URL**

**Local:** `http://localhost:5000`  
**Production:** `https://your-render-service.onrender.com`

---

## **Endpoints**

### **1. GET `/`**

Serve the chatbot web interface.

**Response:**
- `Status: 200 OK`
- `Content-Type: text/html`
- HTML page with chat UI

**Example:**
```bash
curl http://localhost:5000/
```

---

### **2. POST `/chat`**

Send a message and get an AI response. Maintains conversation history via session.

**Request:**
```json
{
  "message": "What is Python?"
}
```

**Response (Success):**
```json
{
  "response": "Python is a high-level programming language known for its simplicity and readability..."
}
```

**Response (Error):**
```json
{
  "error": "Server error: OPENAI_API_KEY environment variable is not set..."
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Empty message
- `500 Internal Server Error` - Server error (see error message)

**Headers:**
```
Content-Type: application/json
```

**Examples:**

```bash
# Basic request
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# With Python
import requests
response = requests.post('http://localhost:5000/chat', 
    json={'message': 'What is AI?'}
)
print(response.json()['response'])

# With JavaScript/Fetch
const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Hello bot!' })
});
const data = await response.json();
console.log(data.response);
```

**Notes:**
- Messages must be non-empty strings
- Conversation history is stored per session (in browser cookies)
- Each message appears in the next request's context

---

### **3. POST `/clear`**

Clear the conversation history for the current session.

**Request:**
```bash
curl -X POST http://localhost:5000/clear
```

**Response:**
```json
{
  "status": "success",
  "message": "Chat history cleared"
}
```

**Status Codes:**
- `200 OK` - Success

**Notes:**
- Deletes session history but keeps the session alive
- Browser cookies remain (session ID is maintained)
- Next message will start a new conversation

---

### **4. GET `/debug`**

Check environment configuration and API key status. **Remove in production.**

**Response (Success):**
```json
{
  "openai_api_key_set": true,
  "flask_env": "production",
  "port": "5000",
  "app_running": true
}
```

**Response (Error - Missing API Key):**
```json
{
  "openai_api_key_set": false,
  "flask_env": "development",
  "port": "5000",
  "app_running": true
}
```

**Status Codes:**
- `200 OK` - Always returns 200

**Usage:**
```bash
# Check if API key is configured
curl http://localhost:5000/debug | python -m json.tool
```

**⚠️ Security Note:** Remove this endpoint in production (`routes/debug` should not exist)

---

## **Session Management**

### **Session Storage**
- **Type:** Filesystem-based (server-side)
- **Location:** `flask_session/` directory
- **Features:** Persists conversation history between requests
- **Cookies:** Browser stores session ID cookie

### **Conversation History Format**
```python
session['history'] = [
    {
        "role": "system",
        "content": "You are a helpful AI..."
    },
    {
        "role": "user",
        "content": "Hello!"
    },
    {
        "role": "assistant",
        "content": "Hi! How can I help?"
    }
]
```

### **Session Lifetime**
- **Default:** Until browser closes
- **Persistent:** Can be extended with `SESSION_PERMANENT = True`
- **Cleanup:** Automatic after 24 hours of inactivity

---

## **Error Handling**

### **Common Errors**

#### **400 Bad Request**
```json
{
  "error": "Empty message"
}
```
**Cause:** Message field missing or empty  
**Fix:** Send non-empty message

#### **500 Internal Server Error**
```json
{
  "error": "Server error: OPENAI_API_KEY environment variable is not set..."
}
```
**Causes:**
- OpenAI API key not configured
- OpenAI API quota exceeded
- Network error
- API service unavailable

**Fix:**
- Check environment variables
- Verify OpenAI account has credits
- Check internet connection
- Test `/debug` endpoint

#### **429 Insufficient Quota**
```json
{
  "error": "Error getting response from AI: Error code: 429 - {'error': {'message': 'You exceeded your current quota...', 'type': 'insufficient_quota'}}"
}
```
**Cause:** OpenAI account has no credits  
**Fix:** Add payment method at https://platform.openai.com/account/billing

---

## **Request/Response Examples**

### **Example 1: Simple Chat**

```bash
# Request
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'

# Response
{
  "response": "The capital of France is Paris. It is located in north-central France along the Seine River and is known for its cultural heritage, architecture, and landmarks like the Eiffel Tower."
}
```

### **Example 2: Multi-turn Conversation**

```bash
# First message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Python"}' \
  -b "session=abc123"

# Response
{
  "response": "Python is a versatile, high-level programming language..."
}

# Second message (conversation remem bered)
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Why is it useful?"}' \
  -b "session=abc123"

# Response
{
  "response": "Python is useful because... (bot remembers previous message about Python)"
}
```

### **Example 3: Clear History**

```bash
# Clear conversation
curl -X POST http://localhost:5000/clear \
  -b "session=abc123"

# Response
{
  "status": "success",
  "message": "Chat history cleared"
}

# Next message starts fresh conversation
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Python"}' \
  -b "session=abc123"
```

---

## **Integration Examples**

### **Python Client**

```python
import requests
import json

class ChatbotClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def send_message(self, message):
        """Send message and get response"""
        response = self.session.post(
            f"{self.base_url}/chat",
            json={"message": message}
        )
        return response.json()["response"]
    
    def clear_history(self):
        """Clear conversation history"""
        return self.session.post(f"{self.base_url}/clear")

# Usage
client = ChatbotClient()
response = client.send_message("Hello!")
print(response)
client.clear_history()
```

### **JavaScript Fetch**

```javascript
async function sendMessage(message) {
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.response;
    } catch (error) {
        return `Error: ${error.message}`;
    }
}

async function clearChat() {
    const response = await fetch('/clear', { method: 'POST' });
    return response.json();
}

// Usage
const response = await sendMessage("What is AI?");
console.log(response);
```

### **cURL Examples**

```bash
# Test API key configuration
curl http://localhost:5000/debug

# Send message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Clear history
curl -X POST http://localhost:5000/clear

# Pretty-print JSON response
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test"}' | python -m json.tool
```

---

## **Rate Limiting**

Currently **no rate limiting** implemented. For production with high traffic:

1. Add rate limiter:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # ...
```

2. Or use proxy-level rate limiting (Cloudflare, Nginx, etc.)

---

## **CORS**

Currently **no CORS restrictions**. If accessing from different origin, add:

```python
from flask_cors import CORS
CORS(app)
```

---

## **API Versioning**

Current version: **1.0** (no versioning in URLs yet)

Future versions may use:
- `/api/v1/chat`
- `/api/v2/chat`

---

## **Monitoring & Logging**

### **Log Locations**
- **Local:** Console output
- **Render:** Service → Logs tab

### **Debug Logging**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Message")   # Detailed info
logger.info("Info")       # General info
logger.warning("Warning") # Warning
logger.error("Error")     # Error
```

---

## **Testing**

### **With curl**
```bash
# Test endpoint availability
curl -i http://localhost:5000/

# Test chat endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

### **With Postman**
1. Create POST request to `http://localhost:5000/chat`
2. Set header: `Content-Type: application/json`
3. Set body: `{"message": "Hello!"}`
4. Click Send

### **With Python unittest**
```python
import unittest
from web_chatbot import app

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_chat_empty_message(self):
        response = self.app.post('/chat', json={'message': ''})
        self.assertEqual(response.status_code, 400)
```

---

## **Performance**

### **Response Times**
- Typical: 1-3 seconds (OpenAI API latency)
- Minimum: 100ms (empty message validation)
- Maximum: 30+ seconds (timeouts)

### **Optimization Tips**
1. Use `gpt-3.5-turbo` instead of `gpt-4` for speed
2. Reduce `max_tokens` to shorter responses
3. Implement response caching for common questions
4. Use async processing for long operations

---

## **Security**

- ✅ API key in environment variables (never logged)
- ✅ Session cookies are HTTPONLY (JavaScript can't access)
- ✅ CSRF protection via Flask-Session
- ✅ Input validation (non-empty messages)
- ✅ HTTPS on production

---

## **Support & Resources**

- **Issues:** GitHub Issues
- **Docs:** See README.md
- **OpenAI API:** https://platform.openai.com/docs
- **Flask:** https://flask.palletsprojects.com

---

**Last Updated:** February 15, 2026  
**API Version:** 1.0
