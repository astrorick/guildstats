import matplotlib
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.figure import Figure
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.text import Text
from matplotlib.transforms import Bbox, IdentityTransform

# surfaces and ink, from the dark dataviz reference palette: regions are cards on a darker page
PAGE = "#0d0d0d"
SURFACE = "#1a1a19"
FRAME = "#383835"
INK = "#f0efec"
INK_SECONDARY = "#c3c2b7"
INK_MUTED = "#898781"
INK_ON_LIGHT = "#0b0b0b"
GRID = "#2c2c2a"

# point sources: base, quest, extra
SOURCE_COLORS = ["#3987e5", "#d95926", "#199e70"]

# one-hue scales, checked with the dataviz palette validator
TABLE_SIZE_CMAP = LinearSegmentedColormap.from_list("tablesize", ["#7b67cc", "#b0a2fe"])
QUESTS_CMAP = LinearSegmentedColormap.from_list("quests", ["#883601", "#b24b0a", "#d8662a", "#fb864d", "#fdb89a"])

# one color per table: the first three stay apart for every viewer, a fourth needs the table letter too
TABLE_COLORS = ["#c98500", "#d55181", "#3987e5", "#0ca30c"]
TABLE_OTHER_COLOR = "#6b6a65"
TABLES_BY_COLOR_ONLY = 3

# mana symbol colors, always shown with their letter
MANA_COLORS = {"W": "#f8f0c8", "U": "#9fd4f5", "B": "#b49bc9", "R": "#f59a85", "G": "#86d0a2", "C": "#8d8a86"}

# a streak is the same quest in this many consecutive games or more, shown in the quest color
STREAK_MIN_GAMES = 2
STREAK_COLOR = SOURCE_COLORS[1]

# sizes: text follows the window height, everything else follows the text
BASE_FONT_SHARE = 1 / 56
BAR_HEIGHT = 0.56
CELL_WIDTH = 0.9
CELL_HEIGHT = 0.8

def applyStyle(fig: Figure) -> None:
    # the same look at any window size
    fontSize = fig.get_figheight() * 72 * BASE_FONT_SHARE
    matplotlib.rcParams.update({
        "font.size": fontSize,
        "text.color": INK,
        "axes.facecolor": SURFACE,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "xtick.labelcolor": INK_SECONDARY,
        "ytick.labelcolor": INK_MUTED,
        "xtick.labelsize": "small",
        "ytick.labelsize": "small",
        "grid.color": GRID,
        "grid.linewidth": fontSize * 0.06,
        "legend.frameon": False,
        "legend.fontsize": "small",
    })
    fig.set_facecolor(PAGE)
    # a margin around the edge, which TVs often crop
    pad = fontSize / 72 * 0.5
    fig.set_layout_engine("constrained", w_pad = pad, h_pad = pad, wspace = 0.02, hspace = 0.02, rect = (0.02, 0.025, 0.96, 0.95))

def fontSize(factor: float = 1.0) -> float:
    return matplotlib.rcParams["font.size"] * factor

def styleAxes(ax: Axes) -> None:
    # no frame, no tick marks
    ax.set_facecolor(SURFACE)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length = 0)

def frameRegions(fig: Figure, regions: list[tuple[str, list[Axes]]]) -> None:
    # a titled card behind each (title, axes) region of a band, like the group boxes in StatManager
    fig.add_artist(_RegionFrames(regions))

def emptyMessage(ax: Axes, text: str) -> None:
    styleAxes(ax)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.5, 0.5, text, transform = ax.transAxes, ha = "center", va = "center", color = INK_MUTED)

def textColorOn(color) -> str:
    # white or near-black, whichever reads better on the fill
    background = _luminance(color)
    onDark = (_luminance(INK) + 0.05) / (background + 0.05)
    onLight = (background + 0.05) / (_luminance(INK_ON_LIGHT) + 0.05)
    return INK if onDark >= onLight else INK_ON_LIGHT

def drawCell(ax: Axes, x: float, y: float, color, edgeColor: str = "none") -> None:
    ax.add_patch(Rectangle(
        (x - CELL_WIDTH / 2, y - CELL_HEIGHT / 2), CELL_WIDTH, CELL_HEIGHT,
        facecolor = color, edgecolor = edgeColor, linewidth = fontSize(0.14) if edgeColor != "none" else 0,
    ))

def drawManaPip(ax: Axes, x: float, y: float, letter: str, transform = None) -> None:
    # a mana symbol: a colored circle with its letter
    transform = transform if transform is not None else ax.transData
    ax.scatter([x], [y], s = pipDiameter() ** 2, color = MANA_COLORS.get(letter, MANA_COLORS["C"]), linewidths = 0, transform = transform, clip_on = False, zorder = 3)
    ax.text(x, y, letter, transform = transform, ha = "center", va = "center_baseline", fontsize = pipDiameter() * 0.55, fontweight = "bold", color = INK_ON_LIGHT, zorder = 4)

def pipDiameter() -> float:
    return fontSize(1.25)

def tableColor(index: int) -> str:
    # tables past the palette share a neutral color and rely on their letter
    return TABLE_COLORS[index] if index < len(TABLE_COLORS) else TABLE_OTHER_COLOR

def tableLettersNeeded(tableCount: int) -> bool:
    # past three tables, colors alone don't keep every pair apart, so squares show the table letter too
    return tableCount > TABLES_BY_COLOR_ONLY

def _luminance(color) -> float:
    channels = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in to_rgb(color)]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

class _RegionFrames(Artist):
    # rounded cards drawn behind their axes, sized after the layout to everything the axes show;
    # cards in the same band share their top and bottom, titles go in the top-left corner
    def __init__(self, regions: list[tuple[str, list[Axes]]]):
        super().__init__()
        self._regions = [
            (Text(text = title, ha = "left", va = "top", fontsize = "large", fontweight = "bold", color = INK_SECONDARY, transform = IdentityTransform()), axes)
            for title, axes in regions
        ]
        self.set_zorder(-1)

    def draw(self, renderer) -> None:
        boxes = [Bbox.union([ax.get_tightbbox(renderer) for ax in axes]) for _, axes in self._regions]
        bottom, top = min(box.y0 for box in boxes), max(box.y1 for box in boxes)
        pad = renderer.points_to_pixels(fontSize(0.7))
        for (title, _), box in zip(self._regions, boxes):
            card = FancyBboxPatch(
                (box.x0 - pad, bottom - pad), box.width + 2 * pad, top - bottom + 2 * pad,
                boxstyle = f"round,pad=0,rounding_size={pad * 0.8}", transform = IdentityTransform(),
                facecolor = SURFACE, edgecolor = FRAME, linewidth = fontSize(0.07),
            )
            card.draw(renderer)
            title.set_figure(self.figure)
            title.set_position((box.x0, top))
            title.draw(renderer)
