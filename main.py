import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.config.config_db import get_db
from api.models.crud import Crud
from api.models.model_challenge import Challenge, DayPurpose, DayPurposePoint
from api.shemas import shemas

app = FastAPI()


@app.post("/", response_model=shemas.CreateChallenge)
async def create_challenge(challenge: shemas.CreateChallenge,
                           day_purposes: list[shemas.DayPurpose],
                           day_point: list[shemas.DayPurposePoint],
                           setting: shemas.SettingChallenge,
                           db: AsyncSession = Depends(get_db)) -> shemas.CreateChallenge:
    crud = Crud(db)
    model = await crud.create(challenge, day_purposes, day_point, setting)
    return model


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1")