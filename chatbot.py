import requests
from datetime import datetime

# API Keys - Replace with your own from:
# Weather: https://openweathermap.org/api
# News: https://newsapi.org/
WEATHER_API_KEY = "5b2379fef77321fc6eb8deaca147d101"
NEWS_API_KEY = "8fb3025f05834eb6a8698df256c8ce6a"


def get_weather(city):
    """Fetch weather data for a city"""
    try:
        if WEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
            return "Please set your OpenWeather API key in the script first!"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            return f"In {city}: {temp}°C, {description.capitalize()}. Humidity: {humidity}%"
        elif response.status_code == 401:
            return "❌ Weather API Error: Invalid API key. Check your WEATHER_API_KEY."
        elif response.status_code == 404:
            return f"❌ City '{city}' not found. Try a different city name."
        else:
            error_data = response.json()
            return f"❌ Weather API Error ({response.status_code}): {error_data.get('message', 'Unknown error')}"
    except requests.exceptions.Timeout:
        return "❌ Weather request timed out. Check your internet connection."
    except requests.exceptions.ConnectionError:
        return "❌ Connection error. Check your internet connection."
    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"


def get_news(topic="general"):
    """Fetch news headlines"""
    try:
        if NEWS_API_KEY == "YOUR_NEWSAPI_KEY":
            return "Please set your NewsAPI key in the script first!"

        url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&language=en&pageSize=3&apiKey={NEWS_API_KEY}"
        response = requests.get(url)

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


def chatbot():
    """A simple chatbot that responds to user input"""

    print("=" * 50)
    print("Welcome to Simple Chatbot!")
    print("Type 'quit' or 'exit' to end the conversation")
    print("Commands: 'weather [city]', 'news [topic]', 'help'")
    print("=" * 50)
    print()

    responses = {
        "hello": "Hi there! How are you doing today?",
        "hi": "Hello! Nice to meet you!",
        "how are you": "I'm doing great! Thanks for asking!",
        "what is your name": "I'm a simple chatbot. No name yet, but you can call me Bot!",
        "who are you": "I'm a simple chatbot here to chat with you!",
        "bye": "Goodbye! Have a great day!",
        "goodbye": "See you later! Take care!",
        "help": "I can chat with you! Try: 'hello', 'weather [city]', 'news [topic]', or 'time'",
        "python": "Python is an awesome programming language!",
        "thanks": "You're welcome!",
        "thank you": "Happy to help!",
        "time": f"Current time: {datetime.now().strftime('%H:%M:%S')}",
    }

    while True:
        user_input = input("\nYou: ").strip().lower()

        if user_input in ["quit", "exit"]:
            print("Bot: Goodbye! Thanks for chatting with me!")
            break

        if not user_input:
            continue

        # Check for weather command
        if user_input.startswith("weather "):
            city = user_input.replace("weather ", "").strip()
            print(f"Bot: {get_weather(city)}")
            continue

        # Check for news command
        if user_input.startswith("news "):
            topic = user_input.replace("news ", "").strip()
            print(f"Bot: {get_news(topic)}")
            continue

        # Check if user input matches any of our responses
        response_found = False
        for keyword, response in responses.items():
            if keyword in user_input:
                print(f"Bot: {response}")
                response_found = True
                break

        if not response_found:
            print(
                "Bot: I'm not sure how to respond to that. Try saying 'hello' or 'help'!")


if __name__ == "__main__":
    chatbot()
