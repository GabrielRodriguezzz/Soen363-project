from fetchDB import fetch_all_articles
from firebase import search_by_country
from firebase import count_by_sentiment
from firebase import *



if __name__ == "__main__":
    #populate firebase db
    #fetch_all_articles()
    #A basic search query on an attribute value.
    #search_by_country("ca")
    #A query that provides some aggregate data (i.e. number of entities satisfying a criteria)
    #count_by_sentiment(0.6)
    #Find top n entities satisfying a criteria, sorted by an attribute.
    #find_top_n_latest_articles_after_date(5, "2024-11-06T00:00:00Z")
    #Simulate a relational group by query in NoSQL (aggregate per category).
    #aggregate_articles_by_category()
    #timed_query(count_by_sentiment, 0.6)
    #timed_query(find_top_n_latest_articles_after_date, 5, "2024-11-06T00:00:00Z")
    #timed_query(aggregate_articles_by_category)
    #timed_query(search_by_country, "ca")

    #timed_full_text_search("climate change")

    # After creating the index
    #timed_full_text_search("climate change")
    print("")



