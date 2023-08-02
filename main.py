import uuid

import uvicorn
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.config.config_db import get_db
from api.models.crud import Crud
from api.shemas import shemas

from notification_api.router.notification import notification

app = FastAPI()
app.include_router(notification)


@app.post("/", response_model=shemas.CreateChallenge)
async def create_challenge(challenge: shemas.CreateChallenge,
                           day_purposes: list[shemas.DayPurpose],
                           day_point: list[shemas.DayPurposePoint],
                           setting: shemas.SettingChallenge,
                           notification: shemas.Notification,
                           db: AsyncSession = Depends(get_db)) -> shemas.CreateChallenge:
    crud = Crud(db)
    model = await crud.create(challenge, day_purposes, day_point, setting, notification)
    return model


@app.put("/update/{id_challenge}", response_model=shemas.CreateChallenge)
async def update_challenge(id_challenge: uuid.UUID,
                           challenge: shemas.CreateChallenge,
                           day_purposes: shemas.DayPurpose,
                           day_point: shemas.DayPurposePoint,
                           setting: shemas.SettingChallenge,
                           db: AsyncSession = Depends(get_db)):
    crud = Crud(db)
    await crud.update_challenge(challenge=challenge,
                                day_point=day_point,
                                day_purpose=day_purposes,
                                setting=setting,
                                id_challenge=id_challenge)


@app.get("/get-all/{user_id}")
async def get_all(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    crud = Crud(db)
    res = await crud.get_all_challenge(user_id)
    return [i for i in res]


@app.get("/get-current-challenge/{user_id}/{challenge_id}", response_model=shemas.Challenge)
async def get_current_challenge(user_id: uuid.UUID, challenge_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    crud = Crud(db)
    model = await crud.get_currnet_challenge(user_id, challenge_id)
    if model is not None:
        return model
    else:
        return HTTPException(
            status_code=403,
            detail="Неправильный запрос")



if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1")
