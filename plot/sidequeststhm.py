import os

import matplotlib.pyplot as plt
import numpy as np

from model.player import Player

OUTPUT_IMAGE_NAME = "sidequest_hist_thematic.png"
COLORBAR = "gist_earth"
THEMATIC_SQ_NAMES = ["Azorius", "Orzhov", "Boros", "Selesnya", "Dimir", "Izzet", "Simic", "Rakdos", "Golgari", "Gruul"]

def _countCompletedQuests(player: Player) -> list[int]:
    counts = {name: 0 for name in THEMATIC_SQ_NAMES}
    for match in player.Matches:
        for quest in match.ThmSq:
            if quest in counts:
                counts[quest] += 1

    return [counts[name] for name in THEMATIC_SQ_NAMES]

def plotThematicSidequestHist(playersList: list[Player], outputFolder: str) -> None:
    """Stacked histogram of thematic sidequest completions per player."""

    totalGames = max((len(p.Matches) for p in playersList), default = 0)

    fig, ax = plt.subplots(figsize = (14, 6))
    ax.grid(axis = "y", linestyle = "--", alpha = 0.5)
    ax.set_axisbelow(True)
    x = np.arange(len(THEMATIC_SQ_NAMES))
    bottoms = np.zeros(len(THEMATIC_SQ_NAMES), dtype = int)
    cmap = plt.get_cmap(COLORBAR)

    for i, player in enumerate(playersList):
        values = np.array(_countCompletedQuests(player), dtype = int)
        bars = ax.bar(x, values, bottom = bottoms, color = cmap(i / len(playersList)))

        for rect, value, bottom in zip(bars, values, bottoms):
            if value == 0:
                continue
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                bottom + value / 2,
                f"{player.Name}: {value}",
                ha = "center", va = "center",
                fontsize = 8, fontweight = "bold", color = "white",
            )

        bottoms += values

    ax.set_xticks(x)
    ax.set_xticklabels(THEMATIC_SQ_NAMES, rotation = 45, ha = "right")
    ax.set_ylabel("Completed Quests")
    fig.suptitle("Thematic Sidequest Completions", fontsize = 14, fontweight = "bold")
    ax.set_title(f"Total matches: {totalGames}", fontsize = 10, style = "italic")

    plt.tight_layout()
    fig.savefig(os.path.join(outputFolder, OUTPUT_IMAGE_NAME), dpi = 600)
    plt.close(fig)
