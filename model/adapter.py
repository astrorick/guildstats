from model.deck import Deck
from model.player import Player

class Adapter:
    def __init__(self, databasePath: str):
        self.DatabasePath = databasePath

    def ReadPlayersList(self) -> list[Player]:
        pass

    def ReadMatchesList(self) -> list:
        pass
