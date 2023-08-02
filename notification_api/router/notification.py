from fastapi import APIRouter

from notification_api.models.model_notification import Notification
from notification_api.config.confi_db import db
from notification_api.shemas.notification import notifications_entity

notification = APIRouter()


@notification.post("/create")
async def create(notifications: Notification):
    await db.values.insert_one(dict(notifications))
    cursor = db.values.find({})
    return await notifications_entity(cursor.to_list(length=100))
