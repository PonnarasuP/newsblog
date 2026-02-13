import requests

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
NEWS_API_KEY = "4d75ef6e78fe47e79de23d5e47fff612"  # Replace with your free API key


def fetch_news_by_categories(country="us", categories=None, page_size=5):
    if categories is None:
        categories = ["general", "business", "entertainment", "health", "science", "sports", "technology"]
    all_news = {}
    for category in categories:
        params = {
            "country": country,
            "category": category,
            "pageSize": page_size,
            "apiKey": NEWS_API_KEY
        }
        response = requests.get(NEWS_API_URL, params=params)
        if response.status_code == 200:
            all_news[category] = response.json().get("articles", [])
        else:
            all_news[category] = []
    return all_news

# Example automation: fetch news every hour and store in a file
import threading, time, json

def automate_news_fetch(interval=3600, output_file="news_data.json"):
    def fetch_and_store():
        while True:
            news = fetch_news_by_categories()
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(news, f)
            time.sleep(interval)
    thread = threading.Thread(target=fetch_and_store, daemon=True)
    thread.start()
