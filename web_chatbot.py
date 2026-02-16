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
# Disable signer to avoid bytes/string errors
app.config['SESSION_USE_SIGNER'] = False
# Use environment variable to control secure cookies in production
app.config['SESSION_COOKIE_SECURE'] = os.getenv(
    'FLASK_ENV', 'development') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY', 'dev-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(
    __file__), 'flask_session')  # Explicit session directory

# Initialize Session
Session(app)

# Initialize OpenAI client lazily on first use (only created when first message arrives)
_openai_client = None


def get_openai_client():
    """
    Get or initialize OpenAI client.

    Lazy initialization ensures the API key is available at runtime
    (important for Render environment variables).

    Returns:
        OpenAI: Initialized OpenAI client

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set
    """
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ OPENAI_API_KEY environment variable is not set. "
                "Please set it in your Render environment variables before running the app."
            )
        # Initialize OpenAI client - simple and direct
        # The library uses api_key automatically
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


# ============================================================================
# Optional: Weather and News APIs (not required for core functionality)
# ============================================================================

# API Keys from environment
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_weather(city):
    """
    Fetch weather data for a city using OpenWeather API.

    Args:
        city (str): City name

    Returns:
        str: Weather information or helpful message if API not configured
    """
    # Check if API key is configured
    if not WEATHER_API_KEY:
        return (
            f"🌤️ Weather API not configured. "
            f"To enable weather lookup:\n"
            f"1. Get free API key: https://openweathermap.org/api\n"
            f"2. Add WEATHER_API_KEY to Render environment variables\n\n"
            f"For now, try asking me: 'Tell me about weather in {city}'"
        )
    
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
            return "❌ Weather API Error: Invalid API key. Please verify WEATHER_API_KEY in environment variables."
        elif response.status_code == 404:
            return f"❌ City '{city}' not found. Try a different city name."
        else:
            return f"❌ Weather API Error ({response.status_code})"
    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"


def get_news(topic="general"):
    """
    Fetch latest news headlines using NewsAPI.

    Args:
        topic (str): Topic to search for

    Returns:
        str: Top 3 news headlines or helpful message if API not configured
    """
    # Check if API key is configured
    if not NEWS_API_KEY:
        return (
            f"📰 News API not configured. "
            f"To enable news lookup:\n"
            f"1. Get free API key: https://newsapi.org\n"
            f"2. Add NEWS_API_KEY to Render environment variables\n\n"
            f"For now, try asking me: 'Tell me about {topic} news'"
        )
    
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
        elif response.status_code == 401:
            return "❌ News API Error: Invalid API key. Please verify NEWS_API_KEY in environment variables."
        else:
            return f"❌ News API Error ({response.status_code}). Please try again later."
    except Exception as e:
        return f"❌ Error fetching news: {str(e)}"
        return f"Error fetching news: {str(e)}"


def get_chatbot_response(messages):
    """
    Get AI-powered response using OpenAI Chat Completions API.

    Maintains full conversation context by sending entire message history.

    Args:
        messages (list): List of message dicts with roles ('system', 'user', 'assistant')

    Returns:
        str: AI response text

    Configuration:
        - Model: gpt-4o-mini (latest, fastest, most affordable)
        - Max tokens: 300 (response length limit)
        - Temperature: 0.7 (balance between creative and consistent)
    """
    try:
        response = get_openai_client().chat.completions.create(
            model="gpt-4o-mini",  # Latest OpenAI model: fast, cheap, smart
            messages=messages,      # Full conversation history
            max_tokens=300,         # Limit response length
            # Creative but not random (0.0 = deterministic, 1.0 = creative)
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response from AI: {str(e)}"


def process_command(user_message):
    """
    Process special commands before sending to OpenAI.

    Commands:
    - "weather [city]" - Get weather for a city
    - "news [topic]" - Get news headlines
    - "time" - Get current time
    - Others - Send to OpenAI

    Args:
        user_message (str): User's message to parse

    Returns:
        tuple: (response_text, is_command) - response and whether it was a command
    """
    message_lower = user_message.lower().strip()

    # Check for weather command
    if message_lower.startswith('weather '):
        city = user_message[8:].strip()  # Get everything after "weather "
        if city:
            return get_weather(city), True
        else:
            return "Please specify a city: weather [city name]", True

    # Check for news command
    if message_lower.startswith('news '):
        topic = user_message[5:].strip()  # Get everything after "news "
        if topic:
            return get_news(topic), True
        else:
            return get_news("general"), True

    # Check for time command
    if message_lower in ['time', 'what time', 'what time is it', 'current time']:
        current_time = datetime.now().strftime("%I:%M %p")
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Current time: {current_time} | Date: {current_date}", True

    # Check for hello/hi
    if message_lower in ['hello', 'hi', 'hey', 'greetings']:
        return "Hello! 👋 I'm your AI assistant. How can I help you today?", True

    # No command detected
    return None, False


@app.route('/')
def home():
    """Render the chatbot web interface."""
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
                    "content": "You are a helpful, friendly, and professional AI assistant. "
                    "Provide clear, concise answers. Be conversational but informative. "
                    "When relevant, ask follow-up questions to better understand user needs."
                }
            ]

        # Check if message is a special command
        command_response, is_command = process_command(user_message)

        if is_command:
            # Use command response directly
            bot_response = command_response
        else:
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
