from matplotlib.axes import Axes

from gui import theme
from model.player import Player

VALUE_COLUMN = 0.4
MAX_NAMES = 3

def drawHighlights(ax: Axes, players: list[Player]) -> None:
    """Tournament records so far, ties listing every name."""

    theme.styleAxes(ax)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    items = [
        ("Most Kills", _best(players, lambda player: sum(game.Kills for game in player.Games))),
        ("Most Wins", _best(players, lambda player: sum(game.Won for game in player.Games))),
        ("Longest Streak", _longestStreak(players)),
        ("Best Game", _bestGame(players)),
        ("Most Style Points", _best(players, lambda player: sum(game.ExtraPoints() for game in player.Games))),
        ("Most Quests", _best(players, lambda player: sum(len(game.GnrSq) + len(game.ThmSq) for game in player.Games if not game.Skipped))),
    ]
    for i, (label, value) in enumerate(items):
        y = 1 - (i + 0.5) / len(items)
        ax.text(0, y, label, ha = "left", va = "center_baseline", color = theme.INK_MUTED)
        ax.text(VALUE_COLUMN, y, value, ha = "left", va = "center_baseline", fontweight = "bold", color = theme.INK)

def _names(names: list[str]) -> str:
    return ", ".join(names) if len(names) <= MAX_NAMES else f"{len(names)} Players"

def _best(players: list[Player], stat) -> str:
    values = [(stat(player), player.Name) for player in players]
    top = max((value for value, _ in values), default = 0)
    if top <= 0:
        return "–"
    return f"{_names([name for value, name in values if value == top])} · {top}"

def _longestStreak(players: list[Player]) -> str:
    best, holders = 0, []
    for player in players:
        for quest, (_, longest) in player.QuestStreaks().items():
            if longest > best:
                best, holders = longest, [(player.Name, quest)]
            elif longest == best:
                holders.append((player.Name, quest))
    if best < 2:
        return "–"
    if len(holders) == 1:
        return f"{holders[0][0]} · {holders[0][1]} ×{best}"
    return f"{_names(list(dict.fromkeys(name for name, _ in holders)))} · ×{best}"

def _bestGame(players: list[Player]) -> str:
    # every player who made the best score, each followed by the games where they made it
    best, holders = 0, {}
    for player in players:
        for number, game in enumerate(player.Games, start = 1):
            points = 0 if game.Skipped else game.TotalPoints()
            if points > best:
                best, holders = points, {}
            if points == best:
                holders.setdefault(player.Name, []).append(f"G{number}")
    if best <= 0:
        return "–"
    names = [f"{name} ({', '.join(games)})" for name, games in holders.items()]
    return f"{_names(names)} · {best}"
