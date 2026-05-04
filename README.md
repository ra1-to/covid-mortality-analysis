# COVID-19 Mortality Analysis 🦠📊

Exploratory data analysis of COVID-19 mortality across 200+ countries using Python and Pandas.

## Overview

This project processes and visualises the **Our World in Data** COVID-19 dataset to answer three key questions:

1. Which countries have the highest case-fatality rates?
2. How does mortality compare across continents?
3. How did daily deaths evolve over time in selected countries?

## Charts

| Chart | Description |
|-------|-------------|
| `chart1_top10_mortality.png` | Top 10 countries by case-fatality rate |
| `chart2_continents.png` | Deaths per million & mortality rate by continent |
| `chart3_evolution.png` | 7-day rolling average of daily deaths (Morocco, Spain, France, Germany) |

## Project Structure

```
covid-mortality-analysis/
│
├── data/
│   ├── owid-covid-data.csv           ← raw dataset (download separately)
│   ├── last_by_country.csv           ← latest mortality metrics per country
│   ├── continents_compare.csv        ← aggregated stats by continent
│   └── evolution_4_countries.csv     ← time-series for selected countries
│
├── outputs/
│   ├── chart1_top10_mortality.png
│   ├── chart2_continents.png
│   └── chart3_evolution.png
│
├── data_processing.py                ← cleaning + feature engineering + export
├── visualisation.py                  ← chart generation
├── requirements.txt
└── README.md
```

## Pipeline

```
raw CSV → column selection → cleaning → feature engineering → EDA exports → visualisation
```

**Key transformations:**
- `ffill` per country for cumulative columns (`total_cases`, `total_deaths`)
- `fillna(0)` for daily counts (`new_cases`, `new_deaths`)
- Removal of OWID regional aggregates (`World`, `Asia`, etc.)
- Derived features: `mortality_rate`, `deaths_per_million`, `new_deaths_7d`

## Dataset

**Source:** [Our World in Data — COVID-19](https://github.com/owid/covid-19-data/tree/master/public/data)  
**Download:**
```python
import pandas as pd
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df = pd.read_csv(url)
df.to_csv("data/owid-covid-data.csv", index=False)
```

## Stack

- Python 3.10+
- Pandas
- NumPy
- Matplotlib

## Setup

```bash
git clone https://github.com/ra1-to/covid-mortality-analysis
cd covid-mortality-analysis
pip install -r requirements.txt
python data_processing.py
python visualisation.py
```

## Author

**Anwar Nafidi** — Information Systems & Big Data, ENSA Berrechid  
[LinkedIn](https://linkedin.com/in/anwar-nafidi-623780378)
