# 📂 Data Directory Setup

This folder contains the raw relational database used for the Formula 1 Analytics project. 

> **Note:** The heavy SQLite database file (`Formula1.sqlite`) is excluded from Git tracking via `.gitignore` to keep the repository lightweight and adhere to GitHub's file size limits.

---

## 📥 How to Get the Dataset

1. Download the official dataset from Kaggle:
   👉 **[Formula 1 Race Data (SQLite) on Kaggle](https://www.kaggle.com/datasets/davidcochran/formula-1-race-data-sqlite)**

2. Extract the downloaded archive.

3. Place the `Formula1.sqlite` file directly inside this directory:
   ```text
   f1-race-analytics/
   └── data/
       └── Formula1.sqlite
