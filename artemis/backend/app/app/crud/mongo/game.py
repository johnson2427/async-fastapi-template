from app.crud.mongo.base import CRUDBase
from app.models.mongo.mysportsfeeds import Games, CreateGames, UpdateGames


class CRUDMongoGame(CRUDBase[Games, CreateGames, UpdateGames]):
    """
    Game CRUD class.
    """


mongo_game_crud = CRUDMongoGame(Games)
