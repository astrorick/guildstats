from dataclasses import dataclass

from model.deck import Deck
from model.match import Match

@dataclass
class Player:
    Name: str
    Decks: list[Deck]
    Matches: list[Match]
