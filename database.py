from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, AI_MONGO_URL

client = None
db = None

# AI database connection
ai_client = None
ai_db = None

async def connect_db():
    global client, db
    if not MONGO_URL:
        raise Exception("MONGO_URL not found")
    
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        # Explicitly set database name to 'SenioCare' as it is missing from the connection string
        db = client["SenioCare"]
        print(f"Connected to MongoDB: {db.name}")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        raise e

async def connect_ai_db():
    global ai_client, ai_db
    if not AI_MONGO_URL:
        raise Exception("AI_MONGO_URL not found")
    
    try:
        ai_client = AsyncIOMotorClient(AI_MONGO_URL)
        # Set database name for AI database
        ai_db = ai_client["ai"]
        print(f"Connected to AI MongoDB: {ai_db.name}")
    except Exception as e:
        print(f"Could not connect to AI MongoDB: {e}")
        raise e

async def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

async def close_ai_db():
    global ai_client
    if ai_client:
        ai_client.close()
        print("AI MongoDB connection closed")

def get_db():
    return db

def get_ai_db():
    return ai_db
