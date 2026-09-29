"""
Kaya identity and LMDI decomposition.

The Kaya identity splits CO2 emissions into four factors:

    CO2 = Population x (GDP / Population) x (Energy / GDP) x (CO2 / Energy)
          people       affluence            energy intensity   carbon intensity

LMDI (Logarithmic Mean Divisia Index, the additive "LMDI-I" version)
then answers: of the total change in emissions between two points in
time, how many tonnes came from each factor? Its big advantage over
simpler methods is that the four effects add up exactly to the actual
change, with nothing left over.

Reference: Ang, B.W. (2005). The LMDI approach to decomposition
analysis: a practical guide. Energy Policy, 33(7), 867-871.
"""
import numpy as np
import pandas as pd

FACTORS = ["Population", "Affluence", "Energy intensity", "Carbon intensity"]


def kaya_factors(population, gdp, energy, co2) -> pd.DataFrame:
    """Return the four Kaya factors. Their product equals co2."""
    return pd.DataFrame({
        "Population": population,
        "Affluence": gdp / population,          # GDP per person
        "Energy intensity": energy / gdp,       # energy used per unit of GDP
        "Carbon intensity": co2 / energy,       # CO2 per unit of energy
    })


def log_mean(a, b):
    """
    Logarithmic mean of a and b: (a - b) / (ln a - ln b).

    It sits between the geometric and arithmetic means, and it's the
    weight that makes the LMDI effects add up exactly. When a == b the
    formula divides zero by zero, so the limit (a itself) is used.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        out = (a - b) / (np.log(a) - np.log(b))
    return np.where(np.isclose(a, b), a, out)


def lmdi(start: pd.DataFrame, end: pd.DataFrame) -> pd.DataFrame:
    """
    Additive LMDI-I decomposition between two points in time.

    `start` and `end` each need columns: population, gdp, energy, co2
    (one row per country, same index). Returns the change in CO2
    attributed to each factor, in the same units as co2, plus the
    actual total change for checking.
    """
    f0 = kaya_factors(start["population"], start["gdp"], start["energy"], start["co2"])
    f1 = kaya_factors(end["population"], end["gdp"], end["energy"], end["co2"])

    weight = log_mean(end["co2"], start["co2"])
    effects = pd.DataFrame(
        {f: weight * np.log(f1[f] / f0[f]) for f in FACTORS}, index=start.index
    )
    effects["Total change"] = end["co2"] - start["co2"]
    return effects
