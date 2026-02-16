from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Flask-Session for production
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = False  # Disable signer to avoid bytes/string errors
# Use environment variable to control secure cookies in production
app.config['SESSION_COOKIE_SECURE'] = os.getenv(
    'FLASK_ENV', 'development') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY', 'dev-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(__file__), 'flask_session')  # Explicit session directory

# Initialize Session
Session(app)

# Initialize OpenAI client lazily on first use
_openai_client = None


def get_openai_client():
    """Get or initialize OpenAI client"""
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ OPENAI_API_KEY environment variable is not set. "
                "Please set it in your Render environment variables before running the app."
            )
        # Initialize OpenAI client - simple and direct
        # The library will use the api_key automatically
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


# API Keys from environment
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_weather(city):
    """Fetch weather data for a city"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            return f"In {city}: {temp}°C, {description.capitalize()}. Humidity: {humidity}%"
        elif response.status_code == 401:
            return "❌ Weather API Error: Invalid API key."
        elif response.status_code == 404:
            return f"❌ City '{city}' not found. Try a different city name."
        else:
            return f"❌ Weather API Error ({response.status_code})"
    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"


def get_news(topic="general"):
    """Fetch news headlines"""
    try:
        url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&language=en&pageSize=3&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            articles = data['articles']

            if not articles:
                return "No news found for that topic."

            news_text = f"📰 Top 3 {topic.capitalize()} News:\n"
            for i, article in enumerate(articles[:3], 1):
                news_text += f"{i}. {article['title']}\n"
            return news_text
        else:
            return "Sorry, I couldn't fetch news."
    except Exception as e:
        return f"Error fetching news: {str(e)}"


def get_chatbot_response(messages):
    """Get chatbot response using OpenAI Chat Completions API with conversation history"""
    try:
        response = get_openai_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response from AI: {str(e)}"


@app.route('/')
def home():
    """Serve the chatbot page"""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """API endpoint for handling chat messages with conversation history"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request - no JSON data'}), 400

        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Empty message'}), 400

        # Initialize conversation history if it doesn't exist
        if 'history' not in session:
            session['history'] = [
                {
                    "role": "system",
                    "content": "You are a helpful and professional AI assistant."
                }
            ]

        # Append user message to history
        session['history'].append({
            "role": "user",
            "content": user_message
        })

        # Get response from OpenAI with full conversation history
        bot_response = get_chatbot_response(session['history'])

        # Append assistant response to history
        session['history'].append({
            "role": "assistant",
            "content": bot_response
        })

        # Save session
        session.modified = True

        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"Error in /chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/clear', methods=['POST'])
def clear():
    """API endpoint for clearing conversation history"""
    session.pop('history', None)
    session.modified = True
    return jsonify({'status': 'success', 'message': 'Chat history cleared'})


@app.route('/debug', methods=['GET'])
def debug():
    """Debug endpoint to check environment variables (remove in production)"""
    return jsonify({
        'openai_api_key_set': bool(os.getenv('OPENAI_API_KEY')),
        'flask_env': os.getenv('FLASK_ENV', 'development'),
        'port': os.getenv('PORT', '5000'),
        'app_running': True
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
