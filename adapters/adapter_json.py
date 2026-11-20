import json
import os
from dataclasses import asdict

from model.database import Database
from model.deck import Deck
from model.event import Event
from model.game import Game
from model.player import Player
from model.table import Table

DATABASE_VERSION = "v0.2.0"

class AdapterJSON:
    DatabasePath: str
    RawData: dict

    def __init__(self, databasePath: str):
        self.DatabasePath = databasePath
        self.Reload()

    @classmethod
    def CreateEmpty(cls, databasePath: str) -> "AdapterJSON":
        # write an empty database with the template format, then load it
        _writeJSON(databasePath, {
            "Database": {"Name": os.path.splitext(os.path.basename(databasePath))[0], "Version": DATABASE_VERSION},
            "Event": {"Name": "", "Date": "", "Location": ""},
            "Tables": [],
            "Players": [],
        })
        return cls(databasePath)

    def Reload(self) -> None:
        # raw data is replaced only if the whole file parses
        with open(self.DatabasePath, "r", encoding = "utf-8") as jsonFile:
            self.RawData = json.load(jsonFile)

    def _save(self) -> None:
        _writeJSON(self.DatabasePath, self.RawData)

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

    def UpdateEventInfo(self, event: Event) -> None:
        self.RawData["Event"] = asdict(event)
        self._save()

    def AddTable(self, table: Table) -> None:
        self.RawData["Tables"].append(asdict(table))
        self._save()

    def UpdateTable(self, index: int, table: Table) -> None:
        # a renamed table is renamed in the recorded games too
        oldName = self.RawData["Tables"][index]["Name"]
        self.RawData["Tables"][index] = asdict(table)
        for playerData in self.RawData["Players"]:
            for gameData in playerData["Games"]:
                if gameData["Table"] == oldName:
                    gameData["Table"] = table.Name
        self._save()

    def AddPlayer(self, name: str, deck: Deck) -> None:
        self.RawData["Players"].append({"Name": name, "Deck": asdict(deck), "Games": []})
        self._save()

    def UpdatePlayer(self, index: int, name: str, deck: Deck) -> None:
        # player games are left untouched
        playerData = self.RawData["Players"][index]
        playerData["Name"] = name
        playerData["Deck"] = asdict(deck)
        self._save()

    def AddGame(self, playerIndex: int, game: Game) -> None:
        self.RawData["Players"][playerIndex]["Games"].append(asdict(game))
        self._save()

def _writeJSON(path: str, data: dict) -> None:
    # write to a temporary file first, so the database is never left half-written
    tempPath = path + ".tmp"
    with open(tempPath, "w", encoding = "utf-8") as jsonFile:
        json.dump(data, jsonFile, indent = 4, ensure_ascii = False)
    os.replace(tempPath, path)
