"""
Step 2: turn the raw files into a clean country-year panel.

What this script does, in order:
  1. Loads the CO2 and energy files.
  2. Removes regional aggregates ("World", "Europe", "High-income
     countries" and so on). They sit in the same column as real
     countries, and leaving them in would double count emissions.
     They are identified by a missing ISO code.
  3. Keeps only the columns we need and merges in energy-mix shares.
  4. Builds a coverage table showing which countries have complete
     data across the analysis window.
  5. Saves:
       data/processed/country_panel.parquet   (all countries, all years)
       data/processed/core_panel.parquet      (complete countries, 1990-2022)
       outputs/tables/coverage_1990_2022.csv

Run from the project root:
    python -m src.clean_data
"""
import pandas as pd

from src.config import (
    CO2_COLUMNS, CORE_COLUMNS, DATA_PROCESSED, DATA_RAW,
    END_YEAR, ENERGY_COLUMNS, START_YEAR, TABLES,
)


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame]:
    co2 = pd.read_csv(DATA_RAW / "owid-co2-data.csv")
    energy = pd.read_csv(DATA_RAW / "owid-energy-data.csv")
    return co2, energy


def keep_countries(df: pd.DataFrame) -> pd.DataFrame:
    """Drop regional aggregates. Real countries have a 3-letter ISO code."""
    is_country = df["iso_code"].notna() & ~df["iso_code"].astype(str).str.startswith("OWID")
    return df.loc[is_country].copy()


def build_panel(co2: pd.DataFrame, energy: pd.DataFrame) -> pd.DataFrame:
    co2 = keep_countries(co2)[CO2_COLUMNS]
    energy = keep_countries(energy)[ENERGY_COLUMNS]

    # Left join: keep every CO2 row, add energy mix where it exists.
    # We join on iso_code + year rather than country name, because
    # names can differ slightly between files; codes do not.
    panel = co2.merge(energy, on=["iso_code", "year"], how="left", validate="one_to_one")
    return panel.sort_values(["country", "year"]).reset_index(drop=True)


def coverage_table(panel: pd.DataFrame) -> pd.DataFrame:
    """For each country: share of years in the window with each core column present."""
    window = panel[panel["year"].between(START_YEAR, END_YEAR)]
    n_years = END_YEAR - START_YEAR + 1

    coverage = (
        window.groupby("country")[CORE_COLUMNS + ["consumption_co2"]]
        .apply(lambda d: d.notna().sum() / n_years)
        .round(3)
    )
    coverage["complete_core"] = coverage[CORE_COLUMNS].eq(1).all(axis=1)
    return coverage.sort_index()


def main() -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    co2, energy = load_raw()
    panel = build_panel(co2, energy)
    coverage = coverage_table(panel)

    complete = coverage.index[coverage["complete_core"]]
    core = panel[
        panel["country"].isin(complete) & panel["year"].between(START_YEAR, END_YEAR)
    ].reset_index(drop=True)

    panel.to_parquet(DATA_PROCESSED / "country_panel.parquet", index=False)
    core.to_parquet(DATA_PROCESSED / "core_panel.parquet", index=False)
    coverage.to_csv(TABLES / f"coverage_{START_YEAR}_{END_YEAR}.csv")

    print(f"Full panel: {panel['country'].nunique()} countries, "
          f"{panel['year'].min()}-{panel['year'].max()}, {len(panel):,} rows")
    print(f"Core panel: {core['country'].nunique()} countries with complete "
          f"{', '.join(CORE_COLUMNS)} for {START_YEAR}-{END_YEAR}")


if __name__ == "__main__":
    main()
