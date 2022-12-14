from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Any, Optional

from app.db.mongo.base_class import PyObjectId


class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Games(MongoBaseModel):
    date: str = Field(...)
    games: Any = Field(...)


class CreateGames(BaseModel):
    _id: str = Field(default=str(ObjectId()))
    date: str = Field(...)
    games: Any = Field(...)

    class Config:
        schema_extra = {
            "date": "11-22-2022",
            "games": {"someGames": "theseGames"},
        }


class UpdateGames(BaseModel):
    date: Optional[str] = Field(...)
    games: Optional[Any] = Field(...)


class GameLogs(BaseModel):
    id: str = Field(alias="_id")
    date: str
    gamelogs: Any


class TeamGameLogs(BaseModel):
    id: str = Field(alias="_id")
    date: str
    team_gamelogs: Any


class GameLines(BaseModel):
    id: str = Field(alias="_id")
    date: str
    gameLines: Any


class Futures(BaseModel):
    id: str = Field(alias="_id")
    date: str
    futures: Any


class PlayerStatsTotals(BaseModel):
    id: str = Field(alias="_id")
    date: str
    playerStatsTotals: Any


class TeamStatsTotals(BaseModel):
    id: str = Field(alias="_id")
    date: str
    teramStatsTotals: Any


class DailyFantasySports(BaseModel):
    id: str = Field(alias="_id")
    date: str
    dfs: Any
    dfs_players: Any
