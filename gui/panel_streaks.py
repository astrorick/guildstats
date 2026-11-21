from matplotlib.axes import Axes

from gui import theme
from model.player import Player

LINES = 6

def drawStreaks(ax: Axes, players: list[Player]) -> None:
    """Ongoing streaks, longest first: the same quest completed in each of a player's last games."""

    theme.styleAxes(ax)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    # one line per ongoing streak; players arrive in standings order, which breaks ties
    streaks = [
        (current, player.Name, quest)
        for player in players
        for quest, (current, _) in player.QuestStreaks().items()
        if current >= theme.STREAK_MIN_GAMES
    ]
    streaks.sort(key = lambda streak: -streak[0])
    if not streaks:
        theme.emptyMessage(ax, "No Ongoing Streaks")
        return

    # a badge with the streak length, then the player and the quest
    shown = streaks if len(streaks) <= LINES else streaks[:LINES - 1]
    for i, (length, name, quest) in enumerate(shown):
        y = 1 - (i + 0.5) / LINES
        badge = ax.text(
            0.01, y, f"×{length}", ha = "left", va = "center_baseline", fontweight = "bold", color = theme.textColorOn(theme.STREAK_COLOR),
            bbox = dict(boxstyle = "round,pad=0.3", facecolor = theme.STREAK_COLOR, edgecolor = "none"),
        )
        nameText = ax.annotate(name, xy = (1, 0), xycoords = badge, xytext = (theme.fontSize(0.9), 0), textcoords = "offset points", va = "bottom", fontweight = "bold", color = theme.INK)
        ax.annotate(quest, xy = (1, 0), xycoords = nameText, xytext = (theme.fontSize(0.5), 0), textcoords = "offset points", va = "bottom", color = theme.INK_SECONDARY)
    if len(shown) < len(streaks):
        ax.text(0.01, 1 - (LINES - 0.5) / LINES, f"+{len(streaks) - len(shown)} More", ha = "left", va = "center_baseline", color = theme.INK_MUTED)
