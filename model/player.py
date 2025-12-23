from model.deck import Deck

class Player:
    def __init__(self, name: str, decks: list[Deck]):
        self.Name = name
        self.Decks = decks
