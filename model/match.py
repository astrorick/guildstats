from dataclasses import dataclass

@dataclass
class Match:
    Skipped: bool; Table: str; Participants: int; DeckUsed: str
    Kills: int; Won: bool; AltWin: bool; Draw: bool; Scooped: bool; BasePoints: int
    GnrSq: list[str]; ThmSq: list[str]; QuestPoints: int; FarmingPoints: int
    StylePoint: int
    
    def TotalPoints(self):
        return self.BasePoints + min(self.QuestPoints + self.FarmingPoints, 3) + (1 if len(self.StylePoint) > 0 else 0)
