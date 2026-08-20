# 🏎️ Formula 1 Historical Race Analytics & AI Insight Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end sports data analytics and augmented AI application built on decades of historical Formula 1 race data from Kaggle. This project combines relational SQL window functions, statistical hypothesis testing, empirical probability modeling, and an interactive **Streamlit web application** featuring a plain-English **AI Strategy Assistant**.

---

## 📌 Executive Summary

Understanding victory conditions and operational efficiency in Formula 1 requires analyzing multi-variable interactions across seasons. This project:
1. **Queries Relational SQLite Data:** Uses advanced window functions (`SUM() OVER()`, `AVG() OVER()`) to track cumulative championship trajectories and driver consistency.
2. **Evaluates Winning Determinants:** Quantifies starting grid advantage via non-parametric correlation metrics ($\rho$) and models empirical win probabilities $P(\text{Win} \mid \text{Grid} = k)$.
3. **Tests Operational Pitstop Efficiency:** Conducts non-parametric hypothesis testing (Kruskal-Wallis $H$-test / Mann-Whitney $U$-test) across major constructor teams.
4. **Delivers AI-Driven Strategic Insights:** Integrates an augmented AI engine (`F1AnalyticsAI`) inside a Streamlit web app to translate complex statistical outputs into plain-English commentary for non-technical stakeholders.

---

## 🔑 Key Findings & Business Insights

* **Grid Advantage & Finishing Position:** * Spearman Rank Correlation confirms a strong positive relationship ($\rho \approx 0.65$, $p < 0.001$) between starting grid spot and race outcome, establishing grid position as a primary predictor of race performance.
* **Empirical Win Distribution:**
  * Drivers starting from **Pole Position (P1)** win historically ~**40-45%** of races. Win probability drops sharply to ~**20%** from P2 and under **10%** outside the top 3.
* **Pitstop Duration & Constructor Variance:**
  * Statistical hypothesis testing across top teams (e.g., Red Bull, Mercedes, Ferrari) reveals significant execution speed and consistency differences ($p < 0.05$), validating that pit crew efficiency provides a measurable advantage.

---

## 🛠️ Project Architecture & Directory Structure

```text
f1-race-analytics/

├── data/
│   └── Formula1.sqlite        # Raw relational SQLite dataset (Git-ignored)
├── notebooks/
│   └── 01_pipeline_eda.ipynb  # Consolidated end-to-end data pipeline & EDA
├── sql/
│   ├── 01_running_constructor_points.sql # Running constructor points window query
│   └── 02_rolling_avg_lap_times.sql     # 3-lap rolling average lap time query
├── src/
│   └── ai_agent.py            # AI Insight Engine (Statistical-to-NLG converter)
├── visuals/                   # Exported high-resolution analytical plots
│   ├── grid_vs_finish_correlation.png
│   ├── win_probability_by_grid.png
│   └── pitstop_duration_by_team.png
├── .gitignore                 # Excludes raw database, virtual envs, checkpoints
├── README.md                  # Comprehensive project documentation
├── app.py                     # Main interactive Streamlit application
└── requirements.txt           # Environment dependencies
