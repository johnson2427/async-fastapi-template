from typing import Any, Dict

from bson import ObjectId
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.crud.mongo.game import mongo_game_crud
from app.db.mongo.session import AsyncIOMotorClient, get_database
from app.db.mongo.base_class import PyObjectId
from app.models.mongo.mysportsfeeds import CreateGames, Games, UpdateGames

router = APIRouter()


@router.post("/", response_description="Add new game", response_model=Games)
async def create_game(
    game: CreateGames, db: AsyncIOMotorClient = Depends(get_database)
) -> Games:
    return await mongo_game_crud.create(coll=db.MySportsFeeds.games, obj_in=game)


@router.get("/", response_description="Get All Games", response_model=List[Games])
async def get_all_games(
    skip: int = 0, limit: int = 100, db: AsyncIOMotorClient = Depends(get_database)
) -> List[Games]:
    games = await mongo_game_crud.get_multi(
        coll=db.MySportsFeeds.games, skip=skip, limit=limit
    )
    return games


@router.get("/{id}", response_description="Get a game by ID", response_model=Games)
async def get_game_by_id(
    id: str, db: AsyncIOMotorClient = Depends(get_database)
) -> Games:
    game = await mongo_game_crud.get(db.MySportsFeeds.games, id)
    if game is None:
        raise HTTPException(404)
    return Games(**game)


@router.patch("/{id}", response_description="Update a game", response_model=Games)
async def update_game(
    id: str, game_update: UpdateGames, db: AsyncIOMotorClient = Depends(get_database)
) -> Games:
    update_game = await mongo_game_crud.get(db.MySportsFeeds.games, id)
    return await mongo_game_crud.update(
        coll=db.MySportsFeeds.games,
        db_obj=Games(**update_game),
        obj_in=game_update,
    )


@router.delete("/{id}", response_description="Delete a game", response_model=Games)
async def delete_game(
    id: str, db: AsyncIOMotorClient = Depends(get_database)
) -> Games:
    return await mongo_game_crud.remove(
        coll=db.MySportsFeeds.games,
        id=id
    )
