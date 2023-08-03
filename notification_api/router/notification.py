from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from celery import Celery

from api.config.config_db import get_db
from api.models.crud import NotificationUser
from notification_api.models.model_notification import notifications_entity
from notification_api.shemas.notification import Notification
from notification_api.config import confi_db

notification = APIRouter(tags=["Notification"])

task_celery = Celery("notification", broker="redis://localhost:6379/0")


@notification.get("/create")
async def create_data_in_mongodb(db: AsyncSession = Depends(get_db)):
    notif = NotificationUser(db)
    res = await notif.get_notification_current_day_week()
    await confi_db.db.values.insert_many([_data_for_mongo(i) for i in res])
    list_data = confi_db.db.values.find({})
    return await notifications_entity(list_data)


def _data_for_mongo(item: Notification):
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
