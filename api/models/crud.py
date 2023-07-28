import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.model_challenge import Challenge, DayPurpose, DayPurposePoint, SettingChallenge, CountUser
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
                     setting: shemas.SettingChallenge):
        model_challenge = Challenge(**challenge.dict())
        await create_commit(model_challenge, self.db)
        settings = await self.create_settings(setting, model_challenge.id)
        day_purp = await self.create_day_purpose(day_purpose, model_challenge.id)

        if settings.limitations:
            await self.create_count_users(model_challenge.id)
        if not day_purp:
            raise HTTPException(
                status_code=403,
                detail="Не указана задача на день"
            )
        else:
            await self.create_day_point(day_point, day_purp.id)
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

    async def create_day_point(self, data: list[shemas.DayPurposePoint], id_day_purpose: uuid.UUID):
        for i in data:
            model = DayPurposePoint(**i.dict(), day_purpose_id=id_day_purpose)
            self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def create_settings(self, data: list[shemas.SettingChallenge], id_challenge: uuid.UUID):
        model = SettingChallenge(**data.dict(), challenge_id=id_challenge)
        return await create_commit(model, self.db)

    async def create_count_users(self, id_challenge: uuid.UUID):
        model = CountUser(challenge_id=id_challenge)
        return await create_commit(model, self.db)
