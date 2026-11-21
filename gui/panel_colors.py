from matplotlib.axes import Axes

from gui import theme
from model.deck import DECK_COLORS
from model.player import Player

COLOR_NAMES = {"W": "White", "U": "Blue", "B": "Black", "R": "Red", "G": "Green", "C": "Colorless"}

def drawColors(ax: Axes, players: list[Player]) -> None:
    """Share of each color across the players' decks, as a pie in mana order."""

    theme.styleAxes(ax)
    colors = [color for color in DECK_COLORS if any(color in player.Deck.Colors for player in players)]
    if not colors:
        theme.emptyMessage(ax, "No Decks Yet")
        return

    # every deck counts once for each of its colors
    decks = [sum(color in player.Deck.Colors for player in players) for color in colors]
    fills = [theme.MANA_COLORS[color] for color in colors]
    _, _, shares = ax.pie(
        decks, labels = [COLOR_NAMES[color] for color in colors], colors = fills, autopct = "%1.0f%%",
        startangle = 90, counterclock = False, labeldistance = 1.12, pctdistance = 0.68,
        wedgeprops = dict(edgecolor = theme.SURFACE, linewidth = theme.fontSize(0.15)),
        textprops = dict(color = theme.INK_SECONDARY),
    )
    for share, fill in zip(shares, fills):
        share.set(color = theme.textColorOn(fill), fontweight = "bold", fontsize = "small")
