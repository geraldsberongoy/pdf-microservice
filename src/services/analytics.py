from firebase_admin import firestore
from src.config.firebase import get_db

def update_counter(doc_id):
    """Updates the download count in Firestore."""
    db = get_db()
    if not db:
        return
    
    try:
        doc_ref = db.collection('document_stats').document(doc_id)
        # Check if doc exists to decide between update (increment) or set (create)
        if doc_ref.get().exists:
            doc_ref.update({
                'download_count': firestore.Increment(1),
                'last_downloaded': firestore.SERVER_TIMESTAMP
            })
        else:
            doc_ref.set({
                'download_count': 1,
                'created_at': firestore.SERVER_TIMESTAMP,
                'last_downloaded': firestore.SERVER_TIMESTAMP
            })
    except Exception as e:
        print(f"⚠️ Analytics Error: {e}")

def get_document_stats(doc_id):
    """Retrieves the download stats for a specific document."""
    db = get_db()
    if not db:
        return None
    
    try:
        doc_ref = db.collection('document_stats').document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return {"download_count": 0}
    except Exception as e:
        print(f"⚠️ Analytics Error: {e}")
        return None
