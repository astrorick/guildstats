from matplotlib.axes import Axes

from gui import theme
from model.game import GENERIC_SQ_NAMES, THEMATIC_SQ_NAMES
from model.player import Player

QUESTS = GENERIC_SQ_NAMES + THEMATIC_SQ_NAMES
AWARD_NAME = "Child of Alara"
GROUP_GAP = 0.5

def drawQuests(ax: Axes, players: list[Player]) -> None:
    """Times each quest was completed, with a ring on ongoing thematic streaks, then a gold star for the Child of Alara award."""

    theme.styleAxes(ax)

    # generic quests, a small gap, thematic quests, another gap, then the award
    columns = [i + (GROUP_GAP if i >= len(GENERIC_SQ_NAMES) else 0) for i in range(len(QUESTS))]
    awardColumn = columns[-1] + 1 + GROUP_GAP
    ax.set_xlim(-0.5, awardColumn + 0.5)
    ax.xaxis.tick_top()
    ax.set_xticks(columns + [awardColumn], QUESTS + [AWARD_NAME])
    for label in ax.get_xticklabels():
        label.set(rotation = 40, ha = "left", va = "bottom", rotation_mode = "anchor")

    # cells shaded by completions, then a star for each player who has the award so far
    counts = [[sum((game.GnrSq + game.ThmSq).count(quest) for game in player.Games if not game.Skipped) for quest in QUESTS] for player in players]
    maxCount = max((count for row in counts for count in row), default = 0)
    for row, player in enumerate(players):
        streaks = player.QuestStreaks()
        for column, quest, count in zip(columns, QUESTS, counts[row]):
            if count == 0:
                continue
            color = theme.QUESTS_CMAP((count - 1) / max(maxCount - 1, 1))
            # generic quests have no streaks
            streak = streaks.get(quest, (0, 0))[0]
            theme.drawCell(ax, column, row, color, theme.INK if streak >= theme.STREAK_MIN_GAMES else "none")
            ax.text(column, row, str(count), ha = "center", va = "center_baseline", fontsize = "small", color = theme.textColorOn(color))
        if player.ChildOfAlara():
            ax.text(awardColumn, row, "★", ha = "center", va = "center_baseline", fontsize = "x-large", color = theme.AWARD_COLOR)
