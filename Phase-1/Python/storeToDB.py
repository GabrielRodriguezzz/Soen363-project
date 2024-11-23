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


# Function to insert authors into the authors table
def insert_authors(cursor, authors):
    # Split the authors string by commas and strip whitespace
    authors = [author.strip() for author in authors.split(",")]
    author_ids = []
    print(authors)
    for author_name in authors:
        if author_name:  # Skip empty strings if there's any
            try:
                cursor.execute("""
                    INSERT INTO authors (name) 
                    VALUES (%s) 
                    ON CONFLICT (name) 
                    DO NOTHING 
                    RETURNING id
                """, (author_name,))
                
                result = cursor.fetchone()

                if result:  # Only append the id if the insertion is successful
                    author_ids.append(result[0])  # Add the author id to the list
                else:
                    # If no result was returned (author already exists), handle it
                    cursor.execute("""
                        SELECT id FROM authors WHERE name = %s
                    """, (author_name,))
                    result = cursor.fetchone()
                    if result:
                        author_ids.append(result[0])  # Add the existing author id to the list

            except Exception as e:
                print(f"Error inserting author {author_name}: {e}")
    
    return author_ids


def insert_article_author(cursor,authors,article_id):
    author_ids =None
    if authors is not None:
        author_ids = insert_authors(cursor, authors) 
    
  
        # Now, insert the many-to-many relationships between authors and articles
        for author_id in author_ids:
            try:
                cursor.execute("""
                    INSERT INTO author_article (author_id, article_id)
                    VALUES (%s, %s)
                    ON CONFLICT (author_id, article_id) DO NOTHING
                """, (author_id, article_id))
            except Exception as e:
                print(f"Error linking author {author_id} to article {article_id}: {e}")
                return False  # Return False to indicate failure
    return True


# Function to insert article into article_worldNews table
def insert_article_worldNews(cursor, article):
    article_id=None
    try:
        cursor.execute("""
            INSERT INTO public.article_worldnewsapi
                       ( title, url, publish_date, article_id, summary, text, image, source_country, language, sentiment, category)
	        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            article['title'],
            article['url'],
            datetime.fromisoformat(article['publish_date'].rstrip('Z')),
            article['id'],
            article.get('summary'),
            article.get('text'),
            article.get('image'),
            article.get('source_country'),
            article.get('language'),
            article.get('sentiment'),
            article.get('category')
        ))
        article_id= cursor.fetchone()
    except Exception as e:
        print(f"Error inserting article from worldNews {article['id']}: {e}")
        return False  # Return False to indicate failure
    if article["author"] is not None:
        author_ids = insert_authors(cursor, article["author"])
    return True #insert_article_author(cursor,article['author'],article_id)
   


# Function to insert article into article_newsAPI table
def insert_article_newsAPI(cursor, article):
    source_id = article['source']['id'] if article['source']['id'] is not None else None
    source_name = article['source']['name']
    source = (str(source_id) if source_id else None, source_name)  # Ensure id is a string
    article_id=None
    try:
        cursor.execute("""
            INSERT INTO public.article_newsapi
            (title, url, publish_date, source, description, url_to_image, content)
	        VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            article['title'],
            article['url'],
            datetime.fromisoformat(article['publishedAt'].rstrip('Z')),
            source,
            article.get('description'),
            article.get('urlToImage'),
            article.get('content')
        ))
        article_id = cursor.fetchone()
    except Exception as e:
        print(f"Error inserting article from newsAPI {article['id']}: {e}")
        return False  # Return False to indicate failure
    if article["author"] is not None:
        author_ids = insert_authors(cursor, article["author"])

    return True #insert_article_author(cursor,article['author'],article_id)

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
                    success = insert_article_newsAPI(cursor, article)
                else: 
                    success = insert_article_worldNews(cursor, article)

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
    #process_all_files_in_folder('./worldNews_json')
    #process_all_files_in_folder('./newsApi_json')
    load_json_to_db('./worldnews_json/articles__news_7555_10055.json')
    load_json_to_db("./newsApi_json/articles2.json")