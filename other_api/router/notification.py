from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.config.config_db import get_db
from api.models.crud import NotificationUser

notification = APIRouter(prefix="/api-notification")


@notification.get("/get_notification")
async def get_notification(db: AsyncSession = Depends(get_db)):
    data = NotificationUser(db)
    res = await data.get_notification_current_day_week()
    return [i for i in res]
