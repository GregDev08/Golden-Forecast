# Golden Forecast - DataScope Solutions

## Context

We are **DataScope Solutions**, an international data analytics consultancy. This project applies supervised Machine Learning to historical gold price data to generate explainable predictions.

## Team

| Role | Name |
|------|------|
| Product Owner | María |
| Scrum Master | Juan |
| Development Team | José, Gema, Joel |

## Business Problem

Predict the price movement of gold (GC=F) using historical data. We approach the problem from two angles:

- **Regression**: predict the closing price (continuous numerical value)
- **Classification**: predict whether the price will go up or down next day (binary)

## Dataset

Historical data of **GC=F** (Gold Futures) via Yahoo Finance, from 2015 to present. Main variables: Open, High, Low, Close, Volume. Enriched with SP500 and USD Index as external features.

## Tech Stack

Python · pandas · numpy · scikit-learn · matplotlib · seaborn · yfinance

## Repository Structure

```
golden-forecast/
├── data/                # Raw and processed data
│   └── README.md        # Data lineage
├── notebooks/           # Pipeline notebooks
├── src/                 # Reusable functions
├── models/              # Trained models (.pkl)
├── slides/              # Final presentation
├── docs/
│   ├── project_handbook.md   # Project governance
│   ├── data_dictionary.md    # Variable definitions
│   └── decision_log.md       # Decision registry
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md
├── README.md
├── ROADMAP.md
├── requirements.txt
└── .gitignore
```

## How to Run

1. Clone the repository
2. `pip install -r requirements.txt`
3. Open and run notebooks in numerical order

## Governance

This project follows an Agile (Scrum) methodology with:
- **Sprint planning** and daily syncs
- **GitHub Flow**: feature branches + PRs with peer review
- **Protected `main`** branch (no direct pushes)
- **Decision Log** documenting all key technical choices
- **Data lineage** tracked for full reproducibility

## License

Academic project for non-commercial use.


---

<p align="center">
  <img src="src/dashboard/assets/banner.png" alt="Golden Forecast Banner" width="800">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pandas-1.5-150458?logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/scikit--learn-1.3-F7931E?logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/XGBoost-1.7-EC1C24?logo=xgboost&logoColor=white" alt="XGBoost">
  <img src="https://img.shields.io/badge/Plotly-5.17-3F4F75?logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Dash-2.14-008DE4?logo=dash&logoColor=white" alt="Dash">
  <img src="https://img.shields.io/badge/Flask-2.3-000000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Yahoo%20Finance-yfinance-6001D2?logo=yahoo&logoColor=white" alt="yfinance">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

## Dashboard

The **Wild-West slot machine** dashboard is available at http://localhost:8050 with the following sections:

- Price: gold chart with RSI, MACD and volatility
- Macro: correlations with DXY, VIX, TNX
- Models: accuracy comparison across 4 models
- Backtest: strategy performance vs Buy and Hold
- Simulation: trading simulator on historical data

To run it:
```bash
python src/dashboard/app.py
```

---

## Version en Espanol

Somos **DataScope Solutions**, consultora internacional de analisis de datos. Este proyecto aplica Machine Learning supervisado sobre datos historicos del oro para generar predicciones explicables.

**Problema de negocio**: predecir el comportamiento del precio del oro (GC=F) usando datos historicos y macroeconomicos (DXY, VIX, TNX). Abordamos el problema desde regresion y clasificacion (binaria y multiclase).

**Dataset**: datos diarios de GC=F, DXY, VIX y TNX via Yahoo Finance desde 2015.

**Dashboard**: tragaperras del lejano oeste en http://localhost:8050 con secciones de precio, macro, modelos, backtest y simulacion.
