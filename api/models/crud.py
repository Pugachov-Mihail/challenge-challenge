import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.orm import selectinload

from api.models.model_challenge import Challenge, DayPurpose, DayPurposePoint, SettingChallenge, CountUser
from api.models.model_notification import Notification
from api.shemas import shemas


async def create_commit(model, db: AsyncSession):
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model


class Crud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self,
                     challenge: shemas.CreateChallenge,
                     day_purpose: list[shemas.DayPurpose],
                     day_point: list[shemas.DayPurposePoint],
                     setting: shemas.SettingChallenge,
                     notification: shemas.Notification):
        model_challenge = Challenge(**challenge.dict())
        await create_commit(model_challenge, self.db)
        settings = await self.create_settings(setting, model_challenge.id)
        await self.create_notification(notification, model_challenge.id)
        day_purp = await self.create_day_purpose(day_purpose, model_challenge.id)

        if settings.limitations:
            await self.create_count_users(model_challenge.id, challenge.user_id)
        if not day_purp:
            raise HTTPException(
                status_code=403,
                detail="Не указана задача на день"
            )
        else:
            await self.create_day_point(day_point, day_purp.id, model_challenge.id)
        return model_challenge

    async def create_day_purpose(self, data: list[shemas.DayPurpose], id_challenge: uuid.UUID):
        if len(data) > 0:
            for i in data:
                model = DayPurpose(**i.dict(), challenge_id=id_challenge)
                self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return model
        return False

    async def create_day_point(self,
                               data: shemas.DayPurposePoint | list[shemas.DayPurposePoint],
                               id_day_purpose: uuid.UUID,
                               challenge: uuid.UUID):
        for i in data:
            model = DayPurposePoint(**i.dict(),
                                    day_purpose_id=id_day_purpose,
                                    challenge_id=challenge)
            self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def create_settings(self, data: shemas.SettingChallenge, id_challenge: uuid.UUID):
        model = SettingChallenge(**data.dict(), challenge_id=id_challenge)
        return await create_commit(model, self.db)

    async def create_notification(self, data: shemas.Notification, id_challenge: uuid.UUID):
        model = Notification(**data.dict(), challenge_id=id_challenge)
        return await create_commit(model, self.db)

    async def create_count_users(self, id_challenge: uuid.UUID, user_id: uuid.UUID):
        model = CountUser(challenge_id=id_challenge, users_list=user_id)
        return await create_commit(model, self.db)

    async def update_challenge(self,
                               challenge: shemas.CreateChallenge,
                               day_purpose: shemas.DayPurpose,
                               day_point: shemas.DayPurposePoint,
                               setting: shemas.SettingChallenge,
                               notification: shemas.Notification,
                               id_challenge: uuid.UUID):
        model = update(Challenge) \
            .where(Challenge.id == id_challenge)\
            .values(title=challenge.title,
                    description=challenge.description,
                    date_end=challenge.date_end,
                    date_update=datetime.datetime.now())
        await self.db.execute(model)
        await self.db.commit()
        id_purpose = await self.__update_day_purpose(day_purpose, id_challenge)
        await self.__update_day_purpose_point(day_point, id_purpose)
        await self.__update_settings(setting, id_challenge)
        await self.__update_notification(notification, id_challenge)

    async def __update_day_purpose(self, day_purpose: shemas.DayPurpose, id_challenge: uuid.UUID):
        model = update(DayPurpose)\
            .where(DayPurpose.challenge_id == id_challenge)\
            .values(title=day_purpose.title)
        await self.db.execute(model)
        await self.db.commit()
        get_id = await self.db.execute(select(Challenge).where(Challenge.id == id_challenge))
        return get_id.scalar()

    async def __update_day_purpose_point(self, day_point: shemas.DayPurposePoint, id_purpose: uuid.UUID):
        model = update(DayPurposePoint)\
            .where(DayPurposePoint.day_purpose_id == id_purpose)\
            .values(title=day_point.title,
                    date_start=day_point.date_start,
                    date_end=day_point.date_end)
        await self.db.execute(model)
        await self.db.commit()

    async def  __update_settings(self, settings: shemas.SettingChallenge, id_challenge: uuid.UUID):
        model = update(SettingChallenge)\
            .where(SettingChallenge.challenge_id == id_challenge)\
            .values(type=settings.type,
                    paid=settings.paid,
                    cost=settings.cost,
                    limitations=settings.limitations,
                    count_user=settings.count_users)
        await self.db.execute(model)
        await self.db.commit()

    async  def __update_notification(self, notification: shemas.Notification, id_challenge: uuid.UUID):
        model = update(Notification)\
            .where(Notification.challenge_id == id_challenge)\
            .values(day_week=notification.day_week,
                    periodicity=notification.periodicity,
                    period=notification.period,
                    time_start=notification.time_start,
                    time_end=notification.time_end)
        await self.db.execute(model)
        await self.db.commit()

    async def get_all_challenge(self, user_id: uuid.UUID):
        challenge = await self.db.execute(
            select(Challenge)
            .where(Challenge.user_id == user_id)
            .options(
                selectinload(Challenge.day_purposes),
                selectinload(Challenge.day_point)
            )
        )
        return challenge.scalars()

    async def get_currnet_challenge(self, user_id: uuid.UUID, challenge_id: uuid.UUID):
        model = await self.db.execute(
            select(Challenge)
            .where(Challenge.id == challenge_id, Challenge.user_id == user_id)
            .options(
                selectinload(Challenge.day_purposes),
                selectinload(Challenge.day_point)
            )
        )

        return model.scalar()
