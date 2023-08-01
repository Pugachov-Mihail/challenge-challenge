from motor.motor_asyncio import AsyncIOMotorClient

from notification_api.config.settings import DATABASE_URL


conn = AsyncIOMotorClient(DATABASE_URL)

db = conn.notification