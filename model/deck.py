from dataclasses import dataclass

@dataclass
class Deck:
    Name: str
    Commander: str
    Colors: list[str]
