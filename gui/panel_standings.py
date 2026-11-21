from matplotlib.axes import Axes
from matplotlib.patches import Patch
from matplotlib.transforms import offset_copy

from gui import theme
from model.deck import DECK_COLORS
from model.player import Player

SOURCE_NAMES = ["Base", "Quest", "Extra"]
LABEL_MIN_SHARE = 0.07

def drawStandings(namesAx: Axes, ax: Axes, players: list[Player]) -> None:
    """Rank, name and deck colors, then total points stacked by source."""

    theme.styleAxes(namesAx)
    theme.styleAxes(ax)
    namesAx.set_xlim(0, 1)
    namesAx.set_xticks([])
    namesAx.set_yticks([])
    ax.set_xticks([])

    # rank, mana pips and name, laid out in points from the left edge; tied players share the best rank
    totals = [player.TotalPoints() for player in players]
    pipStep = theme.pipDiameter() * 1.1
    rankWidth = theme.fontSize(1.4)
    pipSlots = max(len(player.Deck.Colors) for player in players)
    for row, player in enumerate(players):
        namesAx.text(0, row, str(totals.index(totals[row]) + 1), transform = _shifted(namesAx, rankWidth), ha = "right", va = "center_baseline", color = theme.INK_MUTED)
        colors = [color for color in DECK_COLORS if color in player.Deck.Colors]
        for i, color in enumerate(colors):
            theme.drawManaPip(namesAx, 0, row, color, _shifted(namesAx, rankWidth + (i + 0.9) * pipStep))
        namesAx.text(0, row, player.Name, transform = _shifted(namesAx, rankWidth + (pipSlots + 0.6) * pipStep), ha = "left", va = "center_baseline", color = theme.INK)

    # bars stacked by source, values inside segments that fit, total at the tip
    sources = [
        [sum(game.BasePoints for game in player.Games), sum(game.CappedQuestPoints() for game in player.Games), sum(game.ExtraPoints() for game in player.Games)]
        for player in players
    ]
    xmax = max(max(totals), 1) * 1.15
    ax.set_xlim(0, xmax)
    starts = [0] * len(players)
    for i, color in enumerate(theme.SOURCE_COLORS):
        values = [source[i] for source in sources]
        ax.barh(range(len(players)), values, left = starts, height = theme.BAR_HEIGHT, color = color, edgecolor = theme.SURFACE, linewidth = theme.fontSize(0.12))
        for row, (value, start) in enumerate(zip(values, starts)):
            if value >= LABEL_MIN_SHARE * xmax:
                ax.text(start + value / 2, row, str(value), ha = "center", va = "center_baseline", fontsize = "small", color = theme.textColorOn(color))
        starts = [start + value for start, value in zip(starts, values)]
    for row, total in enumerate(totals):
        ax.text(total + xmax * 0.015, row, str(total), ha = "left", va = "center_baseline", fontweight = "bold", color = theme.INK)

    ax.legend(
        handles = [Patch(color = color, label = name) for name, color in zip(SOURCE_NAMES, theme.SOURCE_COLORS)],
        loc = "lower left", bbox_to_anchor = (0, 1), ncols = 3, handlelength = 0.8, handleheight = 0.8, columnspacing = 1.0, borderaxespad = 0.2,
    )

def _shifted(ax: Axes, points: float):
    # data coordinates moved right by a distance in points
    return offset_copy(ax.transData, fig = ax.figure, x = points, units = "points")
