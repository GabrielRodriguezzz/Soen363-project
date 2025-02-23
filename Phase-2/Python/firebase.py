import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()  # For Firestore


# Function to populate data into a specific subcollection
def populate_subcollection(subcollection_name, articles):
  
    for article in articles:
        doc_id = str(article["id"]) 
        db.collection(subcollection_name).add(article)
        print(f"Added article {doc_id} to {subcollection_name}")

def search_by_country(country_code):
    query = db.collection("articlesWorldnewsAPI").where("source_country", "==", country_code)
    res = query.stream()
    data = []
    for doc in res:
        data.append(doc.to_dict())
    print("Articles with source country: {}".format(country_code))
    print(data)

def count_by_sentiment(threshold):
    query = db.collection("articlesWorldnewsAPI").where("sentiment", ">=", threshold).count()
    count_result = query.get()  

    for aggregation_list in count_result:  
        for aggregation in aggregation_list:  
            print(f"Number of articles with sentiment >= {threshold}: {aggregation.value}")
def find_top_n_latest_articles_after_date(n, start_date):
    query = (
        db.collection("articlesWorldnewsAPI")
        .where("publish_date", ">", start_date) 
        .order_by("publish_date", direction=firestore.Query.DESCENDING)  
        .limit(n) 
    )
    results = query.stream()
    data = []
    print(f"Top {n} articles published after {start_date}:")
    for doc in results:
        article = doc.to_dict()
        data.append(article)
    print("{} articles with published date after {} ordered by descending order".format(n, start_date))
    print(data)
def aggregate_articles_by_category():
    query = db.collection("articlesWorldnewsAPI")
    results = query.stream()

    category_counts = {}

    for doc in results:
        article = doc.to_dict()
        category = article.get("category", "Uncategorized")  
        category_counts[category] = category_counts.get(category, 0) + 1

    print("Article counts per category:")
    for category, count in category_counts.items():
        print(f"Category: {category}, Count: {count}")  


def timed_query(query_function, *args):
    start_time = time.time()
    query_function(*args)  
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.4f} seconds")

def add_search_terms_to_articles(subcollection_name):
    query = db.collection(subcollection_name).stream()
    for doc in query:
        data = doc.to_dict()
        search_terms = f"{data.get('title', '').lower()} {data.get('summary', '').lower()}"
        db.collection(subcollection_name).document(doc.id).update({"search_terms": search_terms})

def full_text_search(keyword):
    keyword = keyword.lower()  
    query = db.collection("articlesWorldnewsAPI").where("search_terms", ">=", keyword).where("search_terms", "<=", keyword + "\uf8ff")
    results = query.stream()
    data = []
    for doc in results:
        data.append(doc.to_dict())
    print(f"Results for '{keyword}': {len(data)} articles found")
    return data


def timed_full_text_search(keyword):
    start_time = time.time()
    results = full_text_search(keyword)
    end_time = time.time()
    print(f"Execution time for '{keyword}': {end_time - start_time:.4f} seconds")
    return results

def add_search_terms_to_articles(subcollection_name):
    query = db.collection(subcollection_name).stream()
    for doc in query:
        data = doc.to_dict()
        search_terms = f"{data.get('title', '').lower()} {data.get('summary', '').lower()}"
        try:
            db.collection(subcollection_name).document(doc.id).update({"search_terms": search_terms})
            print(f"Updated document {doc.id} with search_terms")
        except Exception as e:
            print(f"Error updating document {doc.id}: {e}")

def full_text_search(keyword):
    keyword = keyword.lower()
    try:
        query = db.collection("articlesWorldnewsAPI") \
            .where("search_terms", ">=", keyword) \
            .where("search_terms", "<=", keyword + "\uf8ff")
        results = query.stream()
        data = [doc.to_dict() for doc in results]
        print(f"Results for '{keyword}': {len(data)} articles found")
        return data
    except Exception as e:
        print(f"Error executing full-text search: {e}")
        return []


def full_text_search(keyword):
    keyword = keyword.lower()
    try:
        query = db.collection("articlesWorldnewsAPI") \
            .where("search_terms", ">=", keyword) \
            .where("search_terms", "<=", keyword + "\uf8ff")
        results = query.stream()
        data = [doc.to_dict() for doc in results]
        print(f"Results for '{keyword}': {len(data)} articles found")
        return data
    except Exception as e:
        print(f"Error executing full-text search: {e}")
        return []

def timed_full_text_search(keyword):
    start_time = time.time()
    results = full_text_search(keyword)
    end_time = time.time()
    print(f"Execution time for '{keyword}': {end_time - start_time:.4f} seconds")
    return results






       
