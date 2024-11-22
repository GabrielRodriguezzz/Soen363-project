import psycopg2
import json
from datetime import datetime
import os

# Database connection parameters
db_params = {
    'host': 'localhost',      # Change as needed
    'dbname': 'news_DB',# Change as needed
    'user': 'postgres',  # Change as needed
    'password': 'admin', # Change as needed
    'port': 5432              # Default PostgreSQL port
}


# Function to insert author into the authors table
def insert_author(cursor, author_name):
    try:
        cursor.execute("""
            INSERT INTO authors (name) 
            VALUES (%s) 
            ON CONFLICT (name) 
            DO NOTHING 
            RETURNING id
        """, (author_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except psycopg2.Error as e:
        print(f"Error inserting author {author_name}: {e}")
        return None

# Function to insert article into article_worldNews table
def insert_article_worldNews(cursor, article):
    author_id =None
    if article['author'] is not None:
        author_id = insert_author(cursor, article['author']) 
    
    try:
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
            datetime.fromisoformat(article['publish_date'].rstrip('Z')),
            article.get('source_country'),
            article.get('language'),
            article.get('sentiment'),
            article.get('category')
        ))
    except psycopg2.Error as e:
        print(f"Error inserting article {article['id']}: {e}")
        return False  # Return False to indicate failure

    return True

# Function to insert article into article_newsAPI table
def insert_article_newsAPI(cursor, article):
    author_id =None
    if article['author'] is not None:
        author_id = insert_author(cursor, article['author']) 
    
    source_id = article['source']['id'] if article['source']['id'] is not None else None
    source_name = article['source']['name']
    source = (str(source_id) if source_id else None, source_name)  # Ensure id is a string

    try:
        cursor.execute("""
            INSERT INTO article_newsAPI (
                source, author_id, title, description, url, 
                url_to_image, published_at, content
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            source,
            author_id,
            article['title'],
            article.get('description'),
            article['url'],
            article.get('urlToImage'),
            datetime.fromisoformat(article['publishedAt'].rstrip('Z')),
            article.get('content')
        ))
    except psycopg2.Error as e:
        print(f"Error inserting article from newsAPI {article['id']}: {e}")
        return False  # Return False to indicate failure

    return True

# Main function to load JSON and insert data into tables
def load_json_to_db(json_file):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    try:
        # Load JSON data from file
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        for article in data:
            try:
                # Insert article into the appropriate table based on the structure
                if 'source' in article:  # This indicates it's an article from newsAPI
                    success = insert_article_newsAPI(cursor, article)
                else:  # This indicates it's an article for article_worldNews
                    success = insert_article_worldNews(cursor, article)

                # If any insertion failed, roll back the transaction
                if not success:
                    print("Rolling back due to insertion error.")
                    conn.rollback()  # Rollback the transaction and stop further processing
                    return
                
            except psycopg2.Error as e:
                # If there's an error during processing, rollback the transaction and stop further queries
                print(f"Error processing article {article.get('id', 'Unknown')}: {e}")
                conn.rollback()  # Rollback the transaction
                return

        # Commit changes if all inserts are successful
        conn.commit()
        print("All articles inserted successfully.")
    
    except Exception as e:
        print(f"Error processing JSON: {e}")
        conn.rollback()  # Rollback the transaction in case of any error
    
    finally:
        cursor.close()
        conn.close()


def process_all_files_in_folder(folder_path):
    # List all files in the folder
    for filename in os.listdir(folder_path):
        # Create the full file path
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's a file (and not a directory)
        if os.path.isfile(file_path) and file_path.endswith('.json'):
            print(f"Processing file: {file_path}")
            load_json_to_db(file_path)


if __name__ == '__main__':
    #process_all_files_in_folder('./worldNews_json')
    #process_all_files_in_folder('./newsApi_json')
    load_json_to_db("./newsApi_json/articles2.json")
   #load_json_to_db("./worldnews_json/articles__news_53_2553.json")