from dataclasses import dataclass

from model.deck import Deck
from model.game import Game

@dataclass
class Player:
    Name: str
    Deck: Deck
    Games: list[Game]

    def TotalPoints(self) -> int:
        return sum(game.TotalPoints() for game in self.Games)

    def QuestStreaks(self) -> dict[str, tuple[int, int]]:
        # (current, longest) run of consecutive games completing each quest, skipped games don't break a run
        streaks = {}
        for game in self.Games:
            if game.Skipped:
                continue
            completed = set(game.GnrSq) | set(game.ThmSq)
            for quest in completed | set(streaks):
                current, longest = streaks.get(quest, (0, 0))
                current = current + 1 if quest in completed else 0
                streaks[quest] = (current, max(longest, current))
        return streaks
