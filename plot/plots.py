import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model.scorer import PlayerScore


def plot_points_by_table_size(scores: list[PlayerScore], output_path: str) -> None:
    """Stacked bar chart: 4-player vs 3-player point contributions per player."""
    names = [s.name for s in scores]
    pts_4p = [s.points_from_4p for s in scores]
    pts_3p = [s.points_from_3p for s in scores]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(names, pts_4p, label="4-Player Games", color="#4C72B0")
    ax.bar(names, pts_3p, bottom=pts_4p, label="3-Player Games", color="#DD8452")
    ax.set_xlabel("Player")
    ax.set_ylabel("Points")
    ax.set_title("Points by Table Size")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_points_by_source(scores: list[PlayerScore], output_path: str) -> None:
    """Stacked bar chart: points broken down by source per player."""
    names = [s.name for s in scores]
    base = [s.base_points for s in scores]
    gen_sq = [s.generic_sidequest_points for s in scores]
    them_sq = [s.thematic_sidequest_points for s in scores]
    style = [s.style_points for s in scores]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(names, base, label="Base Rules", color="#4C72B0")
    ax.bar(names, gen_sq, bottom=base, label="Generic Sidequests", color="#DD8452")
    bottom2 = [b + g for b, g in zip(base, gen_sq)]
    ax.bar(names, them_sq, bottom=bottom2, label="Thematic Sidequests", color="#55A868")
    bottom3 = [b + t for b, t in zip(bottom2, them_sq)]
    ax.bar(names, style, bottom=bottom3, label="Style Points", color="#C44E52")
    ax.set_xlabel("Player")
    ax.set_ylabel("Points")
    ax.set_title("Points by Source")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
