import worldnewsapi
from worldnewsapi.rest import ApiException
import json
from datetime import datetime

# Replace with your API key
WORLD_NEWS_API_KEY = "f7a02f39f0b94bdca54e32fde89fc0c5"
# Current query (very broad)
text_query = "news"
# add 2500 when done with API key
offset = 10000

# Latest publish date as the fixed reference
fixed_reference_time = "2024-11-20"

# Configure API
config = worldnewsapi.Configuration(api_key={"apiKey": WORLD_NEWS_API_KEY})
client = worldnewsapi.ApiClient(config)
api_instance = worldnewsapi.NewsApi(client)

def save_articles_to_json(articles, file_prefix, offset, new_offset):
    """Save a list of articles to a JSON file with dynamic naming."""
    filename = f"{file_prefix}_{offset}_{new_offset}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)
    print(f"Saved {len(articles)} articles to {filename}")

def fetch_articles(text, language, latest_publish_date, offset, max_articles=500, number_per_request=100):
    """
    Fetch articles using the World News API with pagination.

    :param text: Query text (e.g., 'news', 'technology', etc.).
    :param language: Language filter (e.g., 'en').
    :param latest_publish_date: Fixed reference time for the latest article.
    :param max_articles: Total number of articles to fetch.
    :param number_per_request: Number of articles per API request.
    """
    all_articles = []

    while len(all_articles) < max_articles:
        try:
            # Adjust number of articles for the last batch
            number = min(number_per_request, max_articles - len(all_articles))

            # Fetch articles
            response = api_instance.search_news(
                text=text,
                language=language,
                number=number,
                offset=offset,
                latest_publish_date=latest_publish_date,  # Fixed reference time
                earliest_publish_date="2024-10-25",
                sort="publish-time",
                sort_direction="DESC"
            )

            # Add articles to the list
            if response.news:
                for article in response.news:
                    all_articles.append({
                        "id": article.id,
                        "title": article.title,
                        "summary": article.summary,
                        "text": article.text,
                        "url": article.url,
                        "image": article.image,
                        "publish_date": article.publish_date,
                        "author": article.author,
                        "category": article.category,
                        "language": article.language,
                        "source_country": article.source_country,
                        "sentiment": article.sentiment
                    })

                print(f"Fetched {len(response.news)} articles. Total so far: {len(all_articles)}.")
            else:
                print("No more articles found.")
                break

            # Increment offset for pagination
            offset += number

            # Stop if we've fetched all available articles
            if len(all_articles) >= response.available:
                break

        except ApiException as e:
            print(f"Exception when calling NewsApi->search_news: {e}")
            break

    # Save all fetched articles to a JSON file
    old_offset = offset - max_articles
    save_articles_to_json(all_articles, file_prefix=f"articles__{text}", offset=old_offset, new_offset=offset)
    print("Available articles: " + str(response.available - offset))

# Example Usage
fetch_articles(
    text=text_query, 
    language="en",  # English language
    latest_publish_date=fixed_reference_time,  # Use fixed reference time
    offset=offset,
    max_articles=2500,  # Adjust to limit the number of articles (maximum for a key is ~2400)
    number_per_request=100  # Fetch in batches of 100 (max for API)
)
