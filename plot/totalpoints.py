import os

import matplotlib.pyplot as plt
import numpy as np

from model.player import Player

OUTPUT_IMAGE_NAME = "total_points.png"
COLORBAR = "Set2"
POINT_CATEGORIES = ["Base", "Quest", "Extra"]

def _computePlayerPoints(player: Player) -> tuple[int, int, int]:
    base = quest = extra = 0
    for match in player.Matches:
        if match.Skipped:
            continue
        base += match.BasePoints
        quest += match.QuestPoints
        extra += 1 if len(match.StylePoint) > 0 else 0

    return base, quest, extra

def plotTotalPoints(playersList: list[Player], outputFolder: str) -> None:
    """Stacked histogram of total points per player, split by source."""

    names = [p.Name for p in playersList]
    categoryTotals = {cat: [] for cat in POINT_CATEGORIES}
    for player in playersList:
        base, quest, extra = _computePlayerPoints(player)
        categoryTotals["Base"].append(base)
        categoryTotals["Quest"].append(quest)
        categoryTotals["Extra"].append(extra)

    fig, ax = plt.subplots(figsize = (12, 6))
    ax.grid(axis = "y", linestyle = "--", alpha = 0.5)
    ax.set_axisbelow(True)

    cmap = plt.get_cmap(COLORBAR)
    x = np.arange(len(names))
    bottoms = np.zeros(len(names), dtype = int)

    for i, category in enumerate(POINT_CATEGORIES):
        values = np.array(categoryTotals[category], dtype = int)
        ax.bar(x, values, bottom = bottoms, color = cmap(i), label = category)
        bottoms += values

    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation = 45, ha = "right")
    ax.set_ylabel("Total Points")
    fig.suptitle("Total Points per Player", fontsize = 14, fontweight = "bold")
    ax.set_title("Stacked by source (Base / Quest / Extra)", fontsize = 10, style = "italic")
    ax.legend()

    plt.tight_layout()
    fig.savefig(os.path.join(outputFolder, OUTPUT_IMAGE_NAME), dpi = 600)
    plt.close(fig)
