import psycopg2
import json
from datetime import datetime

# Database connection parameters
db_params = {
    'host': 'localhost',      # Change as needed
    'dbname': 'your_database',# Change as needed
    'user': 'your_username',  # Change as needed
    'password': 'your_password', # Change as needed
    'port': 5432              # Default PostgreSQL port
}

# Function to insert author into the authors table
def insert_author(cursor, author_name):
    cursor.execute("""
        INSERT INTO authors (name) 
        VALUES (%s) 
        ON CONFLICT (name) 
        DO NOTHING RETURNING id
    """, (author_name,))
    result = cursor.fetchone()
    return result[0] if result else None

# Function to insert article into article_worldNews table
def insert_article_worldNews(cursor, article):
    author_id = insert_author(cursor, article['author'])
    
    cursor.execute("""
        INSERT INTO article_worldNews (
            id, author_id, title, summary, text, url, 
            image, publish_date, source_country, language, sentiment, category
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        article['id'],
        author_id,
        article['title'],
        article.get('summary'),
        article.get('text'),
        article['url'],
        article.get('image'),
        datetime.fromisoformat(article['publish_date'].rstrip('Z')),  # Handle the 'Z' timezone suffix
        article.get('source_country'),
        article.get('language'),
        article.get('sentiment'),
        article.get('category')
    ))

# Function to insert article into article_newsAPI table
def insert_article_newsAPI(cursor, article):
    author_id = insert_author(cursor, article['author'])
    
    # Handling source.id and source.name
    source_id = article['source']['id'] if article['source']['id'] is not None else None
    source_name = article['source']['name']

    cursor.execute("""
        INSERT INTO article_newsAPI (
            source, author_id, title, description, url, 
            url_to_image, published_at, content
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        (source_id, source_name),
        author_id,
        article['title'],
        article.get('description'),
        article['url'],
        article.get('urlToImage'),
        datetime.fromisoformat(article['publishedAt'].rstrip('Z')),  # Handle the 'Z' timezone suffix
        article.get('content')
    ))

# Main function to load JSON and insert data into tables
def load_json_to_db(json_file):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    # Load JSON data from file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    for article in data:
        # Insert article into the appropriate table based on the structure
        if 'source' in article:  # This indicates it's an article from newsAPI
            insert_article_newsAPI(cursor, article)
        else:  # This indicates it's an article for article_worldNews
            insert_article_worldNews(cursor, article)
    
    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

# Example usage:
if __name__ == '__main__':
    load_json_to_db('articles.json')