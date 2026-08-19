import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from src.ai_agent import F1AnalyticsAI

# 1. Page Configuration
st.set_page_config(
    page_title="F1 Analytics & AI Assistant", page_icon="🏎️", layout="wide"
)

st.title("🏎️ Formula 1 Historical Analytics & AI Assistant")
st.markdown(
    "Explore historical race probabilities, pitstop efficiency, and automated AI insights."
)


# 2. Cached Data Loader (Prevents reloading DB on every user click)
@st.cache_data
def load_data():
    conn = sqlite3.connect("data/Formula1.sqlite")

    df_results = pd.read_sql_query(
        """
        SELECT r.raceId, r.year, res.driverId, res.constructorId, res.grid, 
               res.positionOrder AS final_position
        FROM results res
        JOIN races r ON res.raceId = r.raceId
        WHERE res.grid > 0;
    """,
        conn,
    )

    # UPDATED: Changed 'pit_stops' to 'pitstops'
    df_pitstops = pd.read_sql_query(
        """
        SELECT p.raceId, r.year, c.name AS constructor_name, (p.milliseconds / 1000.0) AS duration_sec
        FROM pitstops p
        JOIN races r ON p.raceId = r.raceId
        JOIN results res ON p.raceId = res.raceId AND p.driverId = res.driverId
        JOIN constructors c ON res.constructorId = c.constructorId
        WHERE p.milliseconds BETWEEN 15000 AND 40000;
    """,
        conn,
    )

    conn.close()
    return df_results, df_pitstops

df_results, df_pitstops = load_data()
ai_engine = F1AnalyticsAI(df_results, df_pitstops)

# 3. Sidebar Layout
st.sidebar.header("Navigation & Filters")
app_mode = st.sidebar.radio(
    "Select Feature Module:",
    ["Grid Win Probability AI", "Constructor Pitstop Efficiency"],
)

# MODULE 1: Grid Win Probability
if app_mode == "Grid Win Probability AI":
    st.subheader("Starting Grid Position vs. Win Probability")

    selected_grid = st.sidebar.slider(
        "Select Starting Grid Spot:", min_value=1, max_value=20, value=1
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        # Render plot
        fig, ax = plt.subplots(figsize=(6, 4))
        grid_summary = (
            df_results[df_results["grid"] <= 10]
            .groupby("grid")
            .apply(lambda x: (x["final_position"] == 1).mean())
            .reset_index(name="win_prob")
        )

        sns.barplot(
            data=grid_summary,
            x="grid",
            y="win_prob",
            palette="Blues_d",
            ax=ax,
            hue="grid",
            legend=False,
        )
        ax.set_title("Probability of Winning by Grid Spot (P1 - P10)")
        ax.set_ylabel("P(Win)")
        st.pyplot(fig)

    with col2:
        st.subheader("🤖 AI Plain-English Interpretation")
        ai_response = ai_engine.explain_grid_probability(selected_grid)
        st.info(ai_response)

# MODULE 2: Pitstop Efficiency Comparison
elif app_mode == "Constructor Pitstop Efficiency":
    st.subheader("Pitstop Performance & Hypothesis Testing")

    constructors = sorted(df_pitstops["constructor_name"].unique())
    team_1 = st.sidebar.selectbox("Select Team 1:", constructors, index=0)
    team_2 = st.sidebar.selectbox(
        "Select Team 2:", constructors, index=min(1, len(constructors) - 1)
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        filtered_pits = df_pitstops[
            df_pitstops["constructor_name"].isin([team_1, team_2])
        ]
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(
            data=filtered_pits,
            x="constructor_name",
            y="duration_sec",
            palette="Set2",
            ax=ax,
            hue="constructor_name",
        )
        ax.set_title(f"Pitstop Distribution: {team_1} vs {team_2}")
        ax.set_ylabel("Duration (Seconds)")
        st.pyplot(fig)

    with col2:
        st.subheader("🤖 AI Statistical Analysis")
        ai_pit_response = ai_engine.explain_pitstop_performance(team_1, team_2)
        st.success(ai_pit_response)