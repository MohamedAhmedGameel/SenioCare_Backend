import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    # Fallback or error, original was strict
    print("Warning: MONGO_URL is not set.")

AI_MONGO_URL = os.getenv("AI_MONGO_URL")
if not AI_MONGO_URL:
    print("Warning: AI_MONGO_URL is not set.")

PORT = int(os.getenv("PORT", 5000))
JWT_SECRET = os.getenv("JWT_SECRET")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")
