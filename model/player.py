from dataclasses import dataclass

from model.deck import Deck
from model.game import Game

@dataclass
class Player:
    Name: str
    Deck: Deck
    Games: list[Game]
