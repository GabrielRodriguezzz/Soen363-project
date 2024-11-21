from newsapi import NewsApiClient

# Replace with your actual News API key
NEWS_API_KEY = "f732d8e2bedc40d9a19c49d8b43ed463"

try:
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    headlines = newsapi.get_top_headlines(q='technology', language='en', country='us')

    print("News API Test Successful. Sample Headlines:")
    for article in headlines['articles'][:5]:
        print(f"- {article['title']}")
except Exception as e:
    print(f"Error: {e}")
