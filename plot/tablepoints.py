import os
import matplotlib.pyplot as plt
import numpy as np

from model.player import Player

OUTPUT_IMAGE_NAME = "table_points.png"
COLORBAR = "Dark2"
TABLE_SIZES = [3, 4]
TABLE_LABELS = {3: "3-Player Tables", 4: "4-Player Tables"}

def _computePlayerTablePoints(player: Player) -> tuple[dict[int, int], dict[int, int]]:
    points = {size: 0 for size in TABLE_SIZES}
    counts = {size: 0 for size in TABLE_SIZES}
    for match in player.Matches:
        if match.Skipped:
            continue
        if match.Participants not in points:
            continue
        points[match.Participants] += match.TotalPoints()
        counts[match.Participants] += 1

    return points, counts

def plotTablePoints(playersList: list[Player], outputFolder: str) -> None:
    """Stacked histogram of points per player, split by table size."""

    computed = [
        (p.Name + ("*" if any(m.Skipped for m in p.Matches) else ""), *_computePlayerTablePoints(p))
        for p in playersList
    ]
    computed.sort(key = lambda item: sum(item[1].values()), reverse = True)

    names = [name for name, _, _ in computed]
    sizeTotals = {size: [] for size in TABLE_SIZES}
    sizeCounts = {size: [] for size in TABLE_SIZES}
    totalCounts = []
    for _, points, counts in computed:
        totalCounts.append(sum(counts.values()))
        for size in TABLE_SIZES:
            sizeTotals[size].append(points[size])
            sizeCounts[size].append(counts[size])

    fig, ax = plt.subplots(figsize = (12, 6))
    ax.grid(axis = "y", linestyle = "--", alpha = 0.5)
    ax.set_axisbelow(True)

    cmap = plt.get_cmap(COLORBAR)
    x = np.arange(len(names))
    bottoms = np.zeros(len(names), dtype = int)

    for i, size in enumerate(TABLE_SIZES):
        values = np.array(sizeTotals[size], dtype = int)
        ax.bar(x, values, bottom = bottoms, color = cmap(i), label = TABLE_LABELS[size])
        for j, value in enumerate(values):
            if value <= 0:
                continue
            ax.text(
                x[j],
                bottoms[j] + value / 2,
                f"{sizeCounts[size][j]}",
                ha = "center",
                va = "center",
                fontsize = 9,
            )
        bottoms += values

    for j, total in enumerate(totalCounts):
        if bottoms[j] <= 0:
            continue
        ax.text(
            x[j],
            bottoms[j],
            f"{total}",
            ha = "center",
            va = "bottom",
            fontsize = 9,
            fontweight = "bold",
        )

    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation = 45, ha = "right")
    ax.set_ylabel("Total Points")
    fig.suptitle("Total Points per Player", fontsize = 14, fontweight = "bold")
    ax.set_title("Stacked by Table Size", fontsize = 10, style = "italic")
    ax.legend()

    plt.tight_layout()
    fig.savefig(os.path.join(outputFolder, OUTPUT_IMAGE_NAME), dpi = 600)
    plt.close(fig)
