import requests
import json
from datetime import datetime, timedelta

# Replace with your NewsAPI key
API_KEY = "acac41312fa34390aa42c3e984b44d46"
query = "Cybersecurity"

# Base URL for NewsAPI
BASE_URL = "https://newsapi.org/v2/everything"


# File to save articles
ARTICLES_FILE = "articles.json"

# Get current date and subtract 29 days
current_date = datetime.now()
start_date = current_date - timedelta(days=29)

# Load existing articles from file, or initialize an empty list
try:
    with open(ARTICLES_FILE, "r") as file:
        all_articles = json.load(file)
        print(f"Loaded {len(all_articles)} existing articles from {ARTICLES_FILE}.")
except (FileNotFoundError, json.JSONDecodeError):
    all_articles = []
    print("No existing articles found. Starting fresh.")

# Function to fetch articles for a specific date range
def fetch_articles_for_date_range(from_date, to_date):
    params = {
        "q": query,               # Search keyword
        "from": from_date,        # Start date (YYYY-MM-DD)
        "to": to_date,            # End date (YYYY-MM-DD)
        "sortBy": "publishedAt",  # Sort by publication date
        "language": "en",         # Language of the articles
        "apiKey": API_KEY         # API key
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        print(f"From {from_date} to {to_date}: Got {len(articles)} articles.")
        return articles
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

# Helper function to check for duplicates
def is_duplicate(article, all_articles):
    return any(existing["url"] == article["url"] for existing in all_articles)

# Iteratively fetch articles for each day and save them
total_new_articles = 0
api_calls_made = 0  # Track the number of API calls
while start_date <= current_date:
    from_date = start_date.strftime("%Y-%m-%d")
    to_date = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")

    # Fetch articles for the current date range
    articles = fetch_articles_for_date_range(from_date, to_date)
    api_calls_made += 1  # Increment API call counter

    # Filter out duplicates
    new_articles = [article for article in articles if not is_duplicate(article, all_articles)]

    # Append new articles to the main list
    all_articles.extend(new_articles)

    # Update total new articles count
    total_new_articles += len(new_articles)
    print(f"Added {len(new_articles)} new articles from {from_date} to {to_date}. Total articles: {len(all_articles)}")

    # Save to file
    with open(ARTICLES_FILE, "w") as file:
        json.dump(all_articles, file, indent=4)
        print(f"Saved {len(all_articles)} articles to {ARTICLES_FILE}.")

    # Increment the date range
    start_date += timedelta(days=1)

print(f"Script completed. Total new articles added: {total_new_articles}.")
print(f"Total API calls made: {api_calls_made}")
