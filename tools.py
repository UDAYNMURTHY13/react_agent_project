
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default API keys from .env
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# 🧭 Web Search Tool (Tavily API)
def web_search_tool(query: str, api_key: str = None) -> str:
    """
    Searches the web using Tavily API via POST request.
    Returns top 2-3 results with title + snippet + link.
    """
    print(f"🌐 Searching web for: {query}")

    key = api_key or TAVILY_API_KEY
    if not key:
        return "⚠️ Missing TAVILY_API_KEY in .env file"

    try:
        url = "https://api.tavily.com/search"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {"query": query, "limit": 3}

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code != 200:
            return f"⚠️ Web search API error: {response.status_code} - {response.text}"

        data = response.json()
        results = data.get("results", [])
        if not results:
            return "No relevant results found."

        formatted_results = []
        for item in results:
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No snippet")
            link = item.get("link") or item.get("url") or "No link"
            formatted_results.append(f"**{title}** - {snippet}\n🔗 {link}")

        return "\n\n".join(formatted_results)

    except requests.exceptions.RequestException as e:
        return f"⚠️ Web search request error: {str(e)}"
    except Exception as e:
        return f"⚠️ Web search unexpected error: {str(e)}"


# 🌦️ Weather Tool (OpenWeatherMap API)
def weather_tool(city_name: str, api_key: str = None) -> str:
    """
    Fetches real-time weather data from OpenWeatherMap API.
    Returns a short description and temperature.
    """
    print(f"🌦️ Fetching weather for: {city_name}")

    key = api_key or OPENWEATHER_API_KEY
    if not key:
        return "⚠️ Missing OPENWEATHER_API_KEY in .env file"

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city_name,
            "appid": key,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return f"⚠️ Weather API error: {response.status_code} - {response.text}"

        data = response.json()
        if data.get("cod") != 200:
            return f"⚠️ City not found or API error: {data.get('message')}"

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"].capitalize()
        return f"The current weather in {city_name} is {description} with {temp}°C temperature."

    except requests.exceptions.RequestException as e:
        return f"⚠️ Weather request error: {str(e)}"
    except Exception as e:
        return f"⚠️ Weather unexpected error: {str(e)}"


# Manual tool test
if __name__ == "__main__":
    print(web_search_tool("latest AI news"))
    print(weather_tool("Bangalore"))
