import worldnewsapi
from worldnewsapi.rest import ApiException

# Replace with your actual World News API key
WORLD_NEWS_API_KEY = "ccb52ac45e2945a097e69b248259f242"

try:
    # Initialize the API configuration
    config = worldnewsapi.Configuration(api_key={"apiKey": WORLD_NEWS_API_KEY})
    client = worldnewsapi.ApiClient(config)
    api_instance = worldnewsapi.NewsApi(client)

    # Fetch a single article
    response = api_instance.search_news(
        text="technology",
        language="en",
        number=1  # Request only one article
    )

    # Print the title of the first article
    if response.news:
        article = response.news[0]  # Access the first article
        print("Title: " + str(article.title))
    else:
        print("No articles found.")

except ApiException as e:
    print(f"Exception when calling NewsApi->search_news: {e}")