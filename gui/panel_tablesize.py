from matplotlib.axes import Axes
from matplotlib.patches import Patch

from gui import theme
from model.player import Player
from model.table import Table

LABEL_MIN_SHARE = 0.08

def drawTableSize(ax: Axes, players: list[Player], tables: list[Table]) -> None:
    """Points per player stacked by table size, with the games played at each size at the tip."""

    theme.styleAxes(ax)
    ax.set_xticks([])
    sizeOf = {table.Name: table.Size for table in tables}
    sizes = sorted(set(sizeOf.values()))
    if not sizes:
        theme.emptyMessage(ax, "No Tables Yet")
        return
    colors = [theme.TABLE_SIZE_CMAP(i / max(len(sizes) - 1, 1)) for i in range(len(sizes))]

    # points and games per player at each table size
    points = [[sum(game.TotalPoints() for game in player.Games if not game.Skipped and sizeOf.get(game.Table) == size) for size in sizes] for player in players]
    games = [[sum(1 for game in player.Games if not game.Skipped and sizeOf.get(game.Table) == size) for size in sizes] for player in players]

    # stacked bars, segment points where they fit, games per size at the tip
    totals = [sum(row) for row in points]
    xmax = max(max(totals, default = 0), 1) * 1.3
    ax.set_xlim(0, xmax)
    starts = [0] * len(players)
    for i, color in enumerate(colors):
        values = [row[i] for row in points]
        ax.barh(range(len(players)), values, left = starts, height = theme.BAR_HEIGHT, color = color, edgecolor = theme.SURFACE, linewidth = theme.fontSize(0.12))
        for row, (value, start) in enumerate(zip(values, starts)):
            if value >= LABEL_MIN_SHARE * xmax:
                ax.text(start + value / 2, row, str(value), ha = "center", va = "center_baseline", fontsize = "small", color = theme.textColorOn(color))
        starts = [start + value for start, value in zip(starts, values)]
    for row, total in enumerate(totals):
        if sum(games[row]) > 0:
            ax.text(total + xmax * 0.02, row, "+".join(str(count) for count in games[row]), ha = "left", va = "center_baseline", fontsize = "small", color = theme.INK_MUTED)

    # legend with the average points per game at each size
    labels = []
    for i, size in enumerate(sizes):
        played = sum(row[i] for row in games)
        average = f"{sum(row[i] for row in points) / played:.1f}" if played else "–"
        labels.append(f"{size}-Player · {average}/Game")
    ax.legend(
        handles = [Patch(color = color, label = label) for color, label in zip(colors, labels)],
        loc = "lower left", bbox_to_anchor = (0, 1), ncols = 1, handlelength = 0.8, handleheight = 0.8, borderaxespad = 0.2,
    )
