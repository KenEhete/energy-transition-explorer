"""
Shared helpers for building the analysis sample.

These live in one place so every notebook uses exactly the same
country list, the same start and end points, and the same
decoupling rules. Change a setting in config.py and every later
result updates with it.
"""
import pandas as pd

from src.config import AVG_WINDOW, END_YEAR, MIN_POPULATION, START_YEAR


def analysis_sample(core: pd.DataFrame, min_population: int = MIN_POPULATION) -> pd.DataFrame:
    """Keep countries whose population in END_YEAR meets the threshold."""
    pop = core.loc[core["year"] == END_YEAR].set_index("country")["population"]
    keep = pop.index[pop >= min_population]
    return core[core["country"].isin(keep)].reset_index(drop=True)


def endpoint_means(df: pd.DataFrame, columns: list[str], window: int = AVG_WINDOW) -> pd.DataFrame:
    """
    Average each column over the first and last `window` years of the period.

    With window=3 this compares 1990-1992 with 2020-2022.
    With window=1 it compares the single years 1990 and 2022.
    Returns one row per country with columns like gdp_start, gdp_end.
    """
    start = df[df["year"].between(START_YEAR, START_YEAR + window - 1)]
    end = df[df["year"].between(END_YEAR - window + 1, END_YEAR)]

    start_means = start.groupby("country")[columns].mean().add_suffix("_start")
    end_means = end.groupby("country")[columns].mean().add_suffix("_end")
    return start_means.join(end_means)


def classify_decoupling(gdp_start, gdp_end, co2_start, co2_end) -> pd.Series:
    """
    Label each country by how emissions moved relative to the economy.

    Absolute: GDP grew and emissions fell.
    Relative: GDP and emissions both grew, but emissions grew more slowly.
    None:     emissions grew as fast as GDP, or faster.
    GDP fell: the economy shrank, so decoupling doesn't really apply.
    """
    gdp_growth = gdp_end / gdp_start - 1
    co2_growth = co2_end / co2_start - 1

    labels = pd.Series("None", index=gdp_growth.index)
    labels[(gdp_growth > 0) & (co2_growth < gdp_growth)] = "Relative"
    labels[(gdp_growth > 0) & (co2_growth < 0)] = "Absolute"
    labels[gdp_growth <= 0] = "GDP fell"
    return labels
