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

