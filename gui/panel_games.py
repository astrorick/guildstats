from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from gui import theme
from model.player import Player
from model.table import Table

def drawGames(ax: Axes, players: list[Player], tables: list[Table]) -> None:
    """Points scored in each game on a square colored by its table, so players who shared a table share a color."""

    theme.styleAxes(ax)
    count = max((len(player.Games) for player in players), default = 0)
    if count == 0:
        theme.emptyMessage(ax, "No Games Yet")
        return

    # one column per game, labels on top
    ax.set_xlim(-0.5, count - 0.5)
    ax.xaxis.tick_top()
    ax.set_xticks(range(count), [f"G{i + 1}" for i in range(count)])

    # one color per table, in the order the tables were added; table letters too when colors alone aren't enough
    colors = {table.Name: theme.tableColor(i) for i, table in enumerate(tables)}
    withLetters = theme.tableLettersNeeded(len(tables))
    for row, player in enumerate(players):
        for column, game in enumerate(player.Games):
            if game.Skipped:
                ax.text(column, row, "–", ha = "center", va = "center_baseline", color = theme.INK_MUTED)
                continue
            color = colors.get(game.Table, theme.TABLE_OTHER_COLOR)
            theme.drawCell(ax, column, row, color)
            ax.text(
                column + (0.1 if withLetters else 0), row, ("★" if game.Won else "") + str(game.TotalPoints()), ha = "center", va = "center_baseline",
                fontweight = "bold" if game.Won else "normal", color = theme.textColorOn(color),
            )
            if withLetters:
                ax.text(column - theme.CELL_WIDTH / 2 + 0.06, row, game.Table, ha = "left", va = "center_baseline", fontsize = "x-small", color = theme.textColorOn(color))

    # legend above the game labels: each table with its size, then the win star
    handles = [Patch(color = colors[table.Name], label = f"{table.Name} ({table.Size})") for table in tables]
    handles.append(Line2D([], [], linestyle = "none", marker = "*", markersize = theme.fontSize(1.0), color = theme.INK, label = "Win"))
    ax.legend(
        handles = handles, loc = "lower left", bbox_to_anchor = (0, 1), ncols = len(handles),
        handlelength = 0.8, handleheight = 0.8, columnspacing = 1.0, borderaxespad = 1.8,
    )
