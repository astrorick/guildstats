from matplotlib.axes import Axes

from gui import theme
from model.game import GENERIC_SQ_NAMES, THEMATIC_SQ_NAMES
from model.player import Player

QUESTS = GENERIC_SQ_NAMES + THEMATIC_SQ_NAMES
GROUP_GAP = 0.5

def drawQuests(ax: Axes, players: list[Player]) -> None:
    """Times each quest was completed, with a ring on quests in an ongoing streak."""

    theme.styleAxes(ax)

    # generic quests, a small gap, then thematic quests
    columns = [i + (GROUP_GAP if i >= len(GENERIC_SQ_NAMES) else 0) for i in range(len(QUESTS))]
    ax.set_xlim(-0.5, columns[-1] + 0.5)
    ax.xaxis.tick_top()
    ax.set_xticks(columns, QUESTS)
    for label in ax.get_xticklabels():
        label.set(rotation = 40, ha = "left", va = "bottom", rotation_mode = "anchor")

    # cells shaded by completions
    counts = [[sum((game.GnrSq + game.ThmSq).count(quest) for game in player.Games if not game.Skipped) for quest in QUESTS] for player in players]
    maxCount = max((count for row in counts for count in row), default = 0)
    for row, player in enumerate(players):
        streaks = player.QuestStreaks()
        for column, quest, count in zip(columns, QUESTS, counts[row]):
            if count == 0:
                continue
            color = theme.QUESTS_CMAP((count - 1) / max(maxCount - 1, 1))
            theme.drawCell(ax, column, row, color, theme.INK if streaks[quest][0] >= theme.STREAK_MIN_GAMES else "none")
            ax.text(column, row, str(count), ha = "center", va = "center_baseline", fontsize = "small", color = theme.textColorOn(color))
