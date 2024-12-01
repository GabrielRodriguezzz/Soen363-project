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
       
