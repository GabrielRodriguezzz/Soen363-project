import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()  # For Firestore

# Function to create collections and subcollections
def create_collections():
    # Create placeholders for collections/subcollections (if needed for structure)
    parent_collection = db.collection("articles")
    
    # Check if the placeholder document exists before creating it
    if not parent_collection.document("articlesNewsAPI").get().exists:
        parent_collection.document("articlesNewsAPI").set({"initialized": True})  # Placeholder doc
        print("Created articlesNewsAPI collection")
    else:
        print("articlesNewsAPI collection already exists")

    if not parent_collection.document("articlesWorldnewsAPI").get().exists:
        parent_collection.document("articlesWorldnewsAPI").set({"initialized": True})  # Placeholder doc
        print("Created articlesWorldnewsAPI collection")
    else:
        print("articlesWorldnewsAPI collection already exists")


# Function to populate data into a specific subcollection
def populate_subcollection(subcollection_name, articles):
    parent_collection = db.collection("articles")
    subcollection = parent_collection.document(subcollection_name).collection(subcollection_name)

    # Add articles to the subcollection
    for article in articles:
        doc_id = str(article["id"])  # Use the article ID as the document key
        subcollection.document(doc_id).set(article)
        print(f"Added article {doc_id} to {subcollection_name}")

# Example Usage
if __name__ == "__main__":
    # Step 1: Create collections and subcollections
    create_collections()

    # Step 2: Populate subcollections
    # Example data for NewsAPI
    # articles_news_api = [
    #     {"id": 1, "title": "NewsAPI Article 1", "content": "Content of article 1"},
    #     {"id": 2, "title": "NewsAPI Article 2", "content": "Content of article 2"},
    # ]
    # populate_subcollection("articlesNewsAPI", articles_news_api)

    # # Example data for WorldNewsAPI
    # articles_world_news_api = [
    #     {"id": 101, "title": "WorldNewsAPI Article 1", "content": "Content of article 101"},
    #     {"id": 102, "title": "WorldNewsAPI Article 2", "content": "Content of article 102"},
    # ]
    # populate_subcollection("articlesWorldnewsAPI", articles_world_news_api)