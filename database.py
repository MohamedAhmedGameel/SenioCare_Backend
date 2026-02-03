from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = None
db = None

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

async def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_db():
    return db
