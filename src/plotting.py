"""
Shared chart styling, so every figure in the project looks consistent.

Colours come from a colourblind-checked palette. Each category keeps
the same colour in every chart (coal is always the same colour, as is
"absolute decoupling"), so readers never have to relearn a legend.
"""
import matplotlib.pyplot as plt

# Base palette (fixed order, colourblind-checked)
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
MAGENTA = "#e87ba4"
GREY = "#8a8984"
INK = "#0b0b0b"
INK_SOFT = "#52514e"
GRID = "#e4e3df"

# Energy sources (grouped into five so stacked charts stay readable)
ENERGY_COLOURS = {
    "Coal": BLUE,
    "Oil": ORANGE,
    "Gas": AQUA,
    "Nuclear": YELLOW,
    "Renewables": MAGENTA,
}

# Decoupling categories
DECOUPLING_ORDER = ["Absolute", "Relative", "None", "GDP fell"]
DECOUPLING_COLOURS = {
    "Absolute": BLUE,
    "Relative": ORANGE,
    "None": AQUA,
    "GDP fell": GREY,
}


def set_style() -> None:
    """Apply the project's default look to all matplotlib charts."""
    plt.rcParams.update({
        "figure.figsize": (10, 5),
        "figure.dpi": 100,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelcolor": INK_SOFT,
        "axes.edgecolor": GRID,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
        "legend.frameon": False,
        "lines.linewidth": 2,
    })

# Kaya factors: warm colours push emissions up, cool colours pull them down
KAYA_COLOURS = {
    "Population": YELLOW,
    "Affluence": ORANGE,
    "Energy intensity": BLUE,
    "Carbon intensity": AQUA,
}
