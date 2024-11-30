import psycopg2
import json
from firebase import populate_subcollection 

# Replace these with your actual database credentials
db_params = {
    'host': 'localhost',      
    'dbname': 'news_DB',
    'user': 'postgres',  
    'password': 'admin', 
    'port': 5432              
}

def fetch_all_articles():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()


        # Fetch data from 'article_worldNewsAPI' table
        cursor.execute("SELECT * FROM article_worldNewsAPI;")
        worldNewsAPI_articles = cursor.fetchall()
        worldNews_api_articles=[]
        for article in worldNewsAPI_articles:
            article_data = {
                'id': article[0],
                'title': article[1],
                'url': article[2],
                'publish_date': article[3].isoformat() if article[3] else None,
                'author': article[4],
                'article_id':article[5],
                'summary': article[6],
                'text': article[7],
                'image': article[8],
                'source_country': article[9],
                'language': article[10],
                'sentiment': float(article[11]) if article[11] is not None else None,  # Convert Decimal to float
                'category': article[12]
            }
            worldNews_api_articles.append(article_data)

        populate_subcollection("articlesWorldnewsAPI",worldNews_api_articles)
            

        # Fetch data from 'article_newsAPI' table
        cursor.execute("SELECT * FROM article_newsAPI;")
        newsAPI_articles = cursor.fetchall()
        news_api_articles=[]
        for article in newsAPI_articles:
            article_data = {
                'id': article[0],
                'title': article[1],
                'url': article[2],
                'publish_date': article[3].isoformat() if article[3] else None,
                'author': article[4],
                'source': article[5], 
                'description': article[6],
                'url_to_image': article[7],
                'content': article[8]
            }
            newsAPI_articles.append(article_data)
        populate_subcollection("articlesNewsAPI",news_api_articles)


    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the database connection
        cursor.close()
        conn.close()
