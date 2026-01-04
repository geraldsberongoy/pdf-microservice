import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

db = None

def init_firebase():
    global db
    
    # 1. Try Individual Environment Variables (Priority)
    private_key = os.environ.get('FIREBASE_PRIVATE_KEY')
    client_email = os.environ.get('FIREBASE_CLIENT_EMAIL')
    project_id = os.environ.get('FIREBASE_PROJECT_ID')
    
    if private_key and client_email and project_id:
        try:
            # Fix newlines in private key if they are escaped literal "\n"
            # This is common when storing multiline keys in .env files or cloud consoles
            final_private_key = private_key.replace('\\n', '\n')
            
            cred_dict = {
                "type": "service_account",
                "project_id": project_id,
                "private_key": final_private_key,
                "client_email": client_email,
                "token_uri": "https://oauth2.googleapis.com/token",
            }
            
            cred = credentials.Certificate(cred_dict)
            try:
                firebase_admin.get_app()
            except ValueError:
                firebase_admin.initialize_app(cred)
                
            db = firestore.client()
            print("✅ Firebase initialized from Individual Environment Variables")
            return db
        except Exception as e:
            print(f"❌ Failed to load Firebase from Individual variables: {e}")

    # 2. Try Single JSON Environment Variable (FIREBASE_CREDS)
    firebase_creds_str = os.environ.get('FIREBASE_CREDS')
    if firebase_creds_str:
        try:
            cred_dict = json.loads(firebase_creds_str)
            cred = credentials.Certificate(cred_dict)
            try:
                firebase_admin.get_app()
            except ValueError:
                firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("✅ Firebase initialized from FIREBASE_CREDS Env Var")
            return db
        except Exception as e:
            print(f"❌ Failed to load FIREBASE_CREDS: {e}")

    # 3. Try Local File (serviceAccountKey.json)
    if os.path.exists('serviceAccountKey.json'):
        try:
            cred = credentials.Certificate('serviceAccountKey.json')
            try:
                firebase_admin.get_app()
            except ValueError:
                firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("✅ Firebase initialized from local serviceAccountKey.json")
            return db
        except Exception as e:
            print(f"❌ Failed to load local Firebase file: {e}")

    print("⚠️ No valid Firebase credentials found. Analytics will be skipped.")
    db = None
    return db

def get_db():
    return db
