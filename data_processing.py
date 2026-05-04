"""
COVID-19 Mortality Analysis — Data Processing Pipeline

Author  : Anwar Nafidi
Dataset : Our World in Data — COVID-19 (owid-covid-data.csv)
Purpose : Load, clean, engineer features, and export analysis-ready CSVs
"""

import pandas as pd
import numpy as np


# 1. LOAD DATA:

raw = pd.read_csv("data/owid-covid-data.csv")
df  = pd.DataFrame(raw)


# 2. COLUMN SELECTION:

# Keep only the columns relevant to mortality analysis

COLS_KEEP = [
    "location", "date", "continent", "population",
    "total_cases", "new_cases",
    "total_deaths", "new_deaths"
]

cols_drop = [col for col in df.columns if col not in COLS_KEEP]
df.drop(columns=cols_drop, inplace=True)


# 3. CLEANING:

# Daily counts: NaN means no report was filed that day → treat as 0
df[["new_cases", "new_deaths"]] = df[["new_cases", "new_deaths"]].fillna(0)

# Cumulative counts: forward-fill within each country (carry last known value),
# then fill remaining NaN at the start of a country's series with 0
df["total_cases"]  = df.groupby("location")["total_cases"].transform("ffill").fillna(0)
df["total_deaths"] = df.groupby("location")["total_deaths"].transform("ffill").fillna(0)

# continent: propagate the first valid value within each country group
# (OWID regional aggregates like "World" or "Asia" have no continent → drop them)
df["continent"] = df.groupby("location")["continent"].transform("first")
df = df[df["continent"].notna()].copy()


# 4. FEATURE ENGINEERING:

# Case-fatality rate expressed as a percentage
df["mortality_rate"] = df["total_deaths"] / df["total_cases"] * 100

# Replace inf values that arise when total_cases == 0
df["mortality_rate"] = (
    df["mortality_rate"]
    .replace([np.inf, -np.inf], np.nan)
    .fillna(0)
)

# Deaths normalised per million inhabitants (fairer cross-country comparison)
df["deaths_per_million"] = df["total_deaths"] / df["population"] * 1_000_000

# 7-day rolling average of daily deaths per country (smooths reporting noise)
df["new_deaths_7d"] = (
    df.groupby("location")["new_deaths"]
    .transform(lambda x: x.rolling(7, min_periods=1).mean())
)


# 5. ANALYSIS OUTPUTS (exported for visualisation.py):

# Last recorded mortality metrics per country
last_by_country = (
    df.groupby("location")[["mortality_rate", "deaths_per_million"]]
    .last()
    .reset_index()
)

# Average mortality metrics aggregated by continent
continents_compare = df.groupby("continent").agg(
    mortality_rate    = ("mortality_rate",    "mean"),
    deaths_per_million= ("deaths_per_million","mean")
)

# Full time-series for selected countries
COUNTRIES = ["Morocco", "Spain", "France", "Germany"]
evolution_4_countries = df[df["location"].isin(COUNTRIES)]



# 6. EXPORT:

last_by_country.to_csv("data/last_by_country.csv",          index=False)
continents_compare.to_csv("data/continents_compare.csv",    index=True)   # index = continent name
evolution_4_countries.to_csv("data/evolution_4_countries.csv", index=False)

print("Data processing complete. CSVs saved to /data")
