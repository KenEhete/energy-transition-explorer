"""
Central settings for the project.

Everything that might change (file paths, URLs, the analysis window)
lives here, so the other scripts never hard-code these values.
"""
from pathlib import Path

# Project root = the folder that contains src/
ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
MANIFEST = ROOT / "data" / "manifest.json"
FIGURES = ROOT / "outputs" / "figures"
TABLES = ROOT / "outputs" / "tables"

# Source files from Our World in Data's GitHub repositories
SOURCES = {
    "owid-co2-data.csv":
        "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",
    "owid-co2-codebook.csv":
        "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv",
    "owid-energy-data.csv":
        "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv",
    "owid-energy-codebook.csv":
        "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-codebook.csv",
}

# Analysis window.
# 1990: consumption-based emissions start here.
# 2022: last year with GDP data in the OWID file.
START_YEAR = 1990
END_YEAR = 2022

# Columns kept from the CO2 file.
# Units: co2 and consumption_co2 in million tonnes, gdp in
# international-$ (2011 prices), energy in terawatt-hours.
CO2_COLUMNS = [
    "country", "iso_code", "year",
    "population", "gdp",
    "co2", "co2_per_capita", "co2_per_gdp", "co2_per_unit_energy",
    "consumption_co2", "trade_co2", "trade_co2_share",
    "primary_energy_consumption", "energy_per_gdp",
    "coal_co2", "oil_co2", "gas_co2",
]

# Energy-mix columns (percent of primary energy) from the energy file.
ENERGY_COLUMNS = [
    "iso_code", "year",
    "coal_share_energy", "oil_share_energy", "gas_share_energy",
    "nuclear_share_energy", "hydro_share_energy", "wind_share_energy",
    "solar_share_energy", "other_renewables_share_energy",
    "renewables_share_energy", "low_carbon_share_energy",
    "fossil_share_energy",
]

# Columns a country must have for every year in the window
# to be included in the core analysis.
CORE_COLUMNS = ["population", "gdp", "co2", "primary_energy_consumption"]

# --- Sample decisions (set in notebooks/02_data_checks.ipynb) ---
# Countries below this population (in END_YEAR) are left out of the
# analysis sample. Very small economies swing wildly in percentage
# terms and would dominate rankings like "fastest to decarbonise".
MIN_POPULATION = 1_000_000

# Start and end points are averaged over this many years
# (1990-1992 and 2020-2022) so one unusual year can't drive a result.
AVG_WINDOW = 3
