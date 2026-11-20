from dataclasses import dataclass

DECK_COLORS = ["W", "U", "B", "R", "G", "C"]

@dataclass
class Deck:
    Name: str
    Commander: str
    Colors: list[str]
