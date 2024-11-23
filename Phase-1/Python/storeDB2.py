import psycopg2
import json
from datetime import datetime
import os

# Database connection parameters
db_params = {
    'host': 'localhost',      
    'dbname': 'news_DB',
    'user': 'postgres',  
    'password': 'admin', 
    'port': 5432              
}



def insert_article_worldNews(cursor, article,conn):
    try:
        cursor.execute("""
            INSERT INTO article_worldnewsapi
                       ( title, url, publish_date,author, article_id, summary, text, image, source_country, language, sentiment, category)
	        VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            article['title'],
            article['url'],
            datetime.fromisoformat(article['publish_date'].rstrip('Z')),
            article['author'],
            article['id'],
            article.get('summary'),
            article.get('text'),
            article.get('image'),
            article.get('source_country'),
            article.get('language'),
            article.get('sentiment'),
            article.get('category')
        ))
        
        
    except Exception as e:
        print(f"Error inserting article from worldNews {article['id']}: {e}")
        return False  # Return False to indicate failure
    return True
   


# Function to insert article into article_newsAPI table
def insert_article_newsAPI(cursor, article,conn):
    source_id = article['source']['id'] if article['source']['id'] is not None else None
    source_name = article['source']['name']
    source = (str(source_id) if source_id else None, source_name) 
    try:
        cursor.execute("""
            INSERT INTO article_newsapi
            (title, url, publish_date,author, source, description, url_to_image, content)
	        VALUES (%s, %s,%s, %s, %s, %s, %s, %s)
        """, (
            article['title'],
            article['url'],
            datetime.fromisoformat(article['publishedAt'].rstrip('Z')),
            article['author'],
            source,
            article.get('description'),
            article.get('urlToImage'),
            article.get('content')
        ))
    except Exception as e:
        print(f"Error inserting article from newsAPI {article['id']}: {e}")
        return False  # Return False to indicate failure

    return True#insert_article_author(cursor,article['author'],article_id,article["title"])

# Main function to load JSON and insert data into tables
def load_json_to_db(json_file):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        for article in data:
            try:
                if 'source' in article:
                    success = insert_article_newsAPI(cursor, article,conn)
                else: 
                    success = insert_article_worldNews(cursor, article,conn)

                # If any insertion failed, roll back the transaction
                if not success:
                    print("Rolling back due to insertion error.")
                    conn.rollback()
                    return
                
            except Exception as e:
                print(f"Error processing article {article.get('id', 'Unknown')}: {e}")
                conn.rollback() 
                return

        # Commit changes if all inserts are successful
        conn.commit()
        print("All articles inserted successfully.")
    
    except Exception as e:
        print(f"Error processing JSON: {e}")
        conn.rollback()  
    
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
    process_all_files_in_folder('./worldNews_json')
    process_all_files_in_folder('./newsApi_json')