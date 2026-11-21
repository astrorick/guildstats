from dataclasses import dataclass

GENERIC_SQ_NAMES = ["First Blood", "Kill Yourself", "Commander Kill", "Tu Quoque Brute"]
# the ten guilds of Ravnica, each with its two colors
THEMATIC_SQ_COLORS = {
    "Azorius": ["W", "U"], "Orzhov": ["W", "B"], "Boros": ["W", "R"], "Selesnya": ["W", "G"], "Dimir": ["U", "B"],
    "Izzet": ["U", "R"], "Simic": ["U", "G"], "Rakdos": ["B", "R"], "Golgari": ["B", "G"], "Gruul": ["R", "G"],
}
THEMATIC_SQ_NAMES = list(THEMATIC_SQ_COLORS)
STYLE_POINT_NAMES = ["Most Flavorful Play", "Clown Move", "Died With Style", "Poker Face"]

@dataclass
class Game:
    Skipped: bool; Table: str
    Won: bool; AltWin: bool; Draw: bool; Scooped: bool
    Kills: int; GnrSq: list[str]; ThmSq: list[str]
    BasePoints: int; QuestPoints: int; FarmingPoints: int; StylePoint: str

    def CappedQuestPoints(self) -> int:
        # quest and farming points count together up to 3 per game
        return min(self.QuestPoints + self.FarmingPoints, 3)

    def ExtraPoints(self) -> int:
        return 1 if len(self.StylePoint) > 0 else 0

    def TotalPoints(self) -> int:
        return self.BasePoints + self.CappedQuestPoints() + self.ExtraPoints()
