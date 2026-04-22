import matplotlib.pyplot as plt

from model.deck import Deck
from model.player import Player

COLOR_NAMES = ["White", "Blue", "Black", "Red", "Green"]
COLOR_HEXES = ["#F8F4E3", "#0E68AB", "#3B3B3B", "#D3202A", "#00733E"]

def _getDeckByName(userDecks: list[Deck], deckName: str) -> Deck | None:
    for deck in userDecks:
        if deck.Name == deckName:
            return deck
    
    return None

def plotColorDistribution(playersList: list[Player], outputPath: str) -> None:
    """Pie chart of color distribution across played decks."""

    # get total color counts
    colorCounts = {"W": 0, "U": 0, "B": 0, "R": 0, "G": 0}
    for player in playersList:
        for match in player.Matches:
            deckUsed = _getDeckByName(player.Decks, match.DeckUsed)

            if deckUsed == None:
                continue

            for color in deckUsed.Colors:
                colorCounts[color] += 1

    # create figure
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(colorCounts.values(), labels = COLOR_NAMES, colors = COLOR_HEXES, autopct = "%1.1f%%", textprops = {"fontsize": 12})
    for n, t in enumerate(autotexts):
        t.set_color("black") if n == 0 else t.set_color("grey")
        t.set_fontweight("bold")

    ax.set_title("Color Distribution Across Played Decks")

    plt.tight_layout()
    fig.savefig(outputPath, dpi = 600)
    plt.close(fig)
