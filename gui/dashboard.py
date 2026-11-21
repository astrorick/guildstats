from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.gridspec import SubplotSpec

from gui import theme
from gui.panel_colors import drawColors
from gui.panel_games import drawGames
from gui.panel_highlights import drawHighlights
from gui.panel_quests import drawQuests
from gui.panel_standings import drawStandings
from gui.panel_streaks import drawStreaks
from gui.panel_tablesize import drawTableSize
from model.event import Event
from model.player import Player
from model.table import Table

# relative sizes of the header, the region titles, the player rows, the bottom band and the gaps between regions
HEADER_HEIGHT = 1.2
TITLE_HEIGHT = 0.45
ROW_HEIGHT = 0.42
ROWS_EXTRA = 1.0
BOTTOM_HEIGHT = 3.6
ROW_GAP = 0.45
COLUMN_GAP = 0.35
GAME_WIDTH = 0.6
GAME_WIDTH_WITH_LETTERS = 0.8
MIN_ROWS = 6

def drawDashboard(fig: Figure, event: Event, tables: list[Table], players: list[Player]) -> None:
    """The whole StatView: header, one row per player across four regions, then deck colors, highlights and streaks."""

    fig.clear()
    theme.applyStyle(fig)
    players = sorted(players, key = lambda player: (-player.TotalPoints(), player.Name))
    gameCount = max((len(player.Games) for player in players), default = 0)
    rowsHeight = ROW_HEIGHT * max(len(players), MIN_ROWS) + ROWS_EXTRA
    grid = fig.add_gridspec(5, 1, height_ratios = [HEADER_HEIGHT, ROW_GAP, TITLE_HEIGHT + rowsHeight, ROW_GAP, TITLE_HEIGHT + BOTTOM_HEIGHT])
    _drawHeader(fig.add_subplot(grid[0]), event, players, gameCount)

    # player rows, shared by standings, table size, games and quests; empty columns keep the regions apart
    gameWidth = GAME_WIDTH_WITH_LETTERS if theme.tableLettersNeeded(len(tables)) else GAME_WIDTH
    band = grid[2].subgridspec(2, 8, height_ratios = [TITLE_HEIGHT, rowsHeight], width_ratios = [1.2, 3.0, COLUMN_GAP, 3.4, COLUMN_GAP, gameWidth * max(gameCount, 4), COLUMN_GAP, 4.6])
    if players:
        names = fig.add_subplot(band[1, 0])
        bars, tableSize, games, quests = [fig.add_subplot(band[1, column], sharey = names) for column in (1, 3, 5, 7)]
        names.set_ylim(len(players) - 0.5, -0.5)
        drawStandings(names, bars, players)
        drawTableSize(tableSize, players, tables)
        drawGames(games, players, tables)
        drawQuests(quests, players)
        theme.frameRegions(fig, [
            _region(fig, band[0, 0], "Standings by Source", [names, bars]),
            _region(fig, band[0, 3], "Standings by Table Size", [tableSize]),
            _region(fig, band[0, 5], "Games", [games]),
            _region(fig, band[0, 7], "Quests", [quests]),
        ])
    else:
        empty = fig.add_subplot(band[1, :])
        theme.emptyMessage(empty, "No Players Yet")
        theme.frameRegions(fig, [_region(fig, band[0, :], "Standings by Source", [empty])])

    # bottom band: deck colors, highlights, and streaks under the quests
    bottom = grid[4].subgridspec(2, 5, height_ratios = [TITLE_HEIGHT, BOTTOM_HEIGHT], width_ratios = [3.0, COLUMN_GAP, 4.2, COLUMN_GAP, 3.4])
    colors = fig.add_subplot(bottom[1, 0])
    highlights = fig.add_subplot(bottom[1, 2])
    streaks = fig.add_subplot(bottom[1, 4])
    drawColors(colors, players)
    drawHighlights(highlights, players)
    drawStreaks(streaks, players)
    theme.frameRegions(fig, [
        _region(fig, bottom[0, 0], "Deck Color Breakdown", [colors]),
        _region(fig, bottom[0, 2], "Tournament Highlights", [highlights]),
        _region(fig, bottom[0, 4], "Streaks", [streaks]),
    ])

def _region(fig: Figure, titleSpec: SubplotSpec, title: str, axes: list[Axes]) -> tuple[str, list[Axes]]:
    # an empty row on top makes room for the title, so titles line up; the card behind the region draws it
    titleAx = fig.add_subplot(titleSpec)
    titleAx.axis("off")
    return title, [titleAx] + axes

def _drawHeader(ax: Axes, event: Event, players: list[Player], gameCount: int) -> None:
    # event on the left, game status on the right
    ax.axis("off")
    ax.text(0, 0.98, event.Name or "GuildStats", transform = ax.transAxes, ha = "left", va = "top", fontsize = theme.fontSize(2.2), fontweight = "bold", color = theme.INK)
    ax.text(0, 0.05, " · ".join(text for text in (event.Date, event.Location) if text), transform = ax.transAxes, ha = "left", va = "bottom", color = theme.INK_SECONDARY)

    if not players:
        status, detail = "No Players Yet", ""
    elif gameCount == 0:
        status, detail = "Waiting For Game 1", ""
    else:
        reported = sum(len(player.Games) >= gameCount for player in players)
        status = f"Game {gameCount}"
        detail = f"All {len(players)} Results In" if reported == len(players) else f"{reported}/{len(players)} Results In"
    ax.text(1, 0.98, status, transform = ax.transAxes, ha = "right", va = "top", fontsize = theme.fontSize(1.6), fontweight = "bold", color = theme.INK)
    ax.text(1, 0.05, detail, transform = ax.transAxes, ha = "right", va = "bottom", color = theme.INK_SECONDARY)
