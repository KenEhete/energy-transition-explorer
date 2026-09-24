# Global Energy Transition Explorer

Which countries have grown their economies while cutting carbon emissions, and what actually drove the change?

This project uses Our World in Data's CO2 and energy datasets to:

1. Track how countries' energy mix has shifted since 1990
2. Classify countries by decoupling status (absolute, relative, or none)
3. Decompose emission changes into population, affluence, energy intensity and carbon intensity (Kaya identity, LMDI method)
4. Compare production-based and consumption-based emissions to test whether some decarbonisation was offshored

> Status: data pipeline and initial audit complete. Analysis in progress.

## Project structure

```
energy-transition-explorer/
├── data/
│   ├── raw/              # downloaded files (not committed)
│   ├── processed/        # cleaned files (not committed)
│   └── manifest.json     # version record of the data used
├── notebooks/
│   ├── 00_run_pipeline.ipynb
│   └── 01_data_audit.ipynb
├── outputs/
│   ├── figures/
│   └── tables/
├── src/
│   ├── config.py         # paths, URLs, settings
│   ├── download_data.py  # step 1: get the data
│   └── clean_data.py     # step 2: build the country panel
├── requirements.txt
└── README.md
```

## How to reproduce

1. Create a Python environment and install `requirements.txt`
2. Run `notebooks/00_run_pipeline.ipynb` (downloads and cleans the data)
3. Run `notebooks/01_data_audit.ipynb`

Or from a terminal:

```bash
pip install -r requirements.txt
python -m src.download_data
python -m src.clean_data
```

## Data

Our World in Data, CO2 and Greenhouse Gas Emissions dataset and Energy dataset (CC BY 4.0).
- https://github.com/owid/co2-data
- https://github.com/owid/energy-data

The download date and file checksums are recorded in `data/manifest.json`.
