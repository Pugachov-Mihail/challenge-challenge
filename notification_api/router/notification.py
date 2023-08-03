from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.config.config_db import get_db
from api.models.crud import NotificationUser
from notification_api.models.model_notification import notifications_entity
from notification_api.shemas.notification import Notification
from notification_api.config import confi_db

notification = APIRouter(tags=["Notification"])


@notification.get("/create")
async def create(db: AsyncSession = Depends(get_db)):
    notif = NotificationUser(db)
    res = await notif.get_notification_current_day_week()
    for i in res:
        await confi_db.db.values.insert_one(ad(i))
    res_mongo = await confi_db.db.find({})
    return notifications_entity(res_mongo)


def ad(item: Notification):
    return {
        "day_week": item.day_week,
        "periodicity": item.periodicity,
        "period": item.period,
        "time_start": str(item.time_start),
        "time_end": str(item.time_end),
        "challenge": {
            "id": str(item.challenge.id),
            "user_id": str(item.challenge.user_id)
        }
    }
