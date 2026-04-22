import matplotlib.pyplot as plt

from model.player import Player

GENERIC_SQ_NAMES = ["First Blood", "Kill Yourself", "Commander Kill", "Tu Quoque Brute"]
THEMATIC_SQ_NAMES = ["Azorius", "Orzhov", "Boros", "Selesnya", "Dimir", "Izzet", "Simic", "Rakdos", "Golgari", "Gruul"]

def plotSidequestPies(playersList: list[Player], outputPath: str) -> None:
    """Two histograms for generic and thematic sidequest completion counts."""

    plt.tight_layout()
    fig.savefig(outputPath, dpi = 600)
    plt.close(fig)
