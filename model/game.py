from dataclasses import dataclass

GENERIC_SQ_NAMES = ["First Blood", "Kill Yourself", "Commander Kill", "Tu Quoque Brute"]
THEMATIC_SQ_NAMES = ["Azorius", "Orzhov", "Boros", "Selesnya", "Dimir", "Izzet", "Simic", "Rakdos", "Golgari", "Gruul"]

@dataclass
class Game:
    Skipped: bool; Table: str
    Won: bool; AltWin: bool; Draw: bool; Scooped: bool
    Kills: int; GnrSq: list[str]; ThmSq: list[str]
    BasePoints: int; QuestPoints: int; FarmingPoints: int; StylePoint: str

    def TotalPoints(self):
        return self.BasePoints + min(self.QuestPoints + self.FarmingPoints, 3) + (1 if len(self.StylePoint) > 0 else 0)
