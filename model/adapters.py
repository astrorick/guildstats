import json

from model.deck import Deck
from model.match import Match
from model.player import Player

class AdapterJSON:
    DatabasePath: str
    RawData: dict
    
    def __init__(self, databasePath: str):
        self.DatabasePath = databasePath
        self._load()

    def _load(self) -> dict:
        with open(self.DatabasePath, "r") as jsonFile:
            self.RawData = json.load(jsonFile)
    
    def DatabaseInfo(self) -> dict:
        return self.RawData["Info"]

    def PlayersList(self) -> list[Player]:
        playersList = []
        for playerName, playerData in self.RawData["Players"].items():
            # read player decks
            playerDecks = []
            for deckName, deckInfo in playerData["Decks"].items():
                playerDecks.append(Deck(deckName, deckInfo["Commander"], deckInfo["Colors"]))

            # read player matches
            playerMatches = []
            for match in playerData["Matches"]:
                playerMatches.append(
                    Match(
                        Skipped = match["Skipped"],
                        Table = match["Table"],
                        Participants = match["Participants"],
                        DeckUsed = match["DeckUsed"],
                        Kills = match["Kills"],
                        Won = match["Won"],
                        AltWin = match["AltWin"],
                        Draw = match["Draw"],
                        Scooped = match["Scooped"],
                        BasePoints = match["BasePoints"],
                        GnrSq = match["GnrSq"],
                        ThmSq = match["ThmSq"],
                        QuestPoints = match["QuestPoints"],
                        FarmingPoints = match["FarmingPoints"],
                        StylePoint = match["StylePoint"],
                    )
                )
            
            # add player to list
            playersList.append(
                Player(
                    Name = playerName,
                    Decks = playerDecks,
                    Matches = playerMatches,
                )
            )
        
        return playersList
