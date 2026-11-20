import json

from model.database import Database
from model.deck import Deck
from model.event import Event
from model.game import Game
from model.player import Player
from model.table import Table

class AdapterJSON:
    DatabasePath: str
    RawData: dict

    def __init__(self, databasePath: str):
        self.DatabasePath = databasePath
        self._load()

    def _load(self) -> None:
        with open(self.DatabasePath, "r") as jsonFile:
            self.RawData = json.load(jsonFile)

    def DatabaseInfo(self) -> Database:
        database = self.RawData["Database"]
        return Database(
            Name = database["Name"],
            Version = database["Version"],
        )

    def EventInfo(self) -> Event:
        event = self.RawData["Event"]
        return Event(
            Name = event["Name"],
            Date = event["Date"],
            Location = event["Location"],
        )

    def TablesList(self) -> list[Table]:
        return [
            Table(
                Name = table["Name"],
                Size = table["Size"],
            )
            for table in self.RawData["Tables"]
        ]

    def PlayersList(self) -> list[Player]:
        playersList = []
        for playerData in self.RawData["Players"]:
            # read player deck
            deck = playerData["Deck"]
            playerDeck = Deck(
                Name = deck["Name"],
                Commander = deck["Commander"],
                Colors = deck["Colors"],
            )

            # read player games
            playerGames = []
            for gameData in playerData["Games"]:
                playerGames.append(
                    Game(
                        Skipped = gameData["Skipped"],
                        Table = gameData["Table"],
                        Won = gameData["Won"],
                        AltWin = gameData["AltWin"],
                        Draw = gameData["Draw"],
                        Scooped = gameData["Scooped"],
                        Kills = gameData["Kills"],
                        GnrSq = gameData["GnrSq"],
                        ThmSq = gameData["ThmSq"],
                        BasePoints = gameData["BasePoints"],
                        QuestPoints = gameData["QuestPoints"],
                        FarmingPoints = gameData["FarmingPoints"],
                        StylePoint = gameData["StylePoint"],
                    )
                )

            # add player to list
            playersList.append(
                Player(
                    Name = playerData["Name"],
                    Deck = playerDeck,
                    Games = playerGames,
                )
            )

        return playersList
