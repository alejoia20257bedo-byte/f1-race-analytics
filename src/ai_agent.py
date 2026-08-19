import numpy as np
import pandas as pd
from scipy import stats


class F1AnalyticsAI:

    def __init__(self, df_results, df_pitstops):
        self.df_results = df_results
        self.df_pitstops = df_pitstops

    def explain_grid_probability(self, selected_grid):
        """Generates a plain-English explanation for win probability from a specific grid spot."""
        grid_data = self.df_results[self.df_results["grid"] == selected_grid]
        total_starts = len(grid_data)

        if total_starts == 0:
            return f"No historical race starts recorded for Grid Position {selected_grid}."

        wins = len(grid_data[grid_data["final_position"] == 1])
        win_rate = (wins / total_starts) * 100

        # Calculate comparative advantage against P1
        p1_data = self.df_results[self.df_results["grid"] == 1]
        p1_win_rate = (
            len(p1_data[p1_data["final_position"] == 1]) / len(p1_data)
        ) * 100

        insight = (
            f"**AI Strategy Analysis for Starting Position P{selected_grid}:**\n\n"
            f"- Historical Win Rate: **{win_rate:.1f}%** ({wins} victories out of {total_starts} starts).\n"
        )

        if selected_grid == 1:
            insight += "- Starting on **Pole Position (P1)** gives a driver the highest historical advantage, avoiding mid-pack traffic in Turn 1."
        else:
            diff = p1_win_rate - win_rate
            insight += f"- Drivers starting from P{selected_grid} face a **{diff:.1f}% lower probability of victory** compared to starting on Pole Position (P1)."

        return insight

    def explain_pitstop_performance(self, constructor_a, constructor_b):
        """Performs statistical comparison and formats plain-English commentary."""
        team_a_stops = self.df_pitstops[
            self.df_pitstops["constructor_name"] == constructor_a
        ]["duration_sec"].dropna()
        team_b_stops = self.df_pitstops[
            self.df_pitstops["constructor_name"] == constructor_b
        ]["duration_sec"].dropna()

        if len(team_a_stops) < 5 or len(team_b_stops) < 5:
            return "Insufficient sample size to compare these two constructors."

        avg_a = team_a_stops.mean()
        avg_b = team_b_stops.mean()

        # Perform Mann-Whitney U test (non-parametric comparison)
        u_stat, p_val = stats.mannwhitneyu(team_a_stops, team_b_stops)

        faster_team = constructor_a if avg_a < avg_b else constructor_b
        slower_team = constructor_b if avg_a < avg_b else constructor_a
        diff = abs(avg_a - avg_b)

        insight = (
            f"**AI Pitstop Comparison ({constructor_a} vs. {constructor_b}):**\n\n"
            f"- **{constructor_a} Average Stop:** {avg_a:.2f} seconds\n"
            f"- **{constructor_b} Average Stop:** {avg_b:.2f} seconds\n"
            f"- **Delta:** {faster_team} is faster by **{diff:.2f} seconds** per stop on average.\n\n"
        )

        if p_val < 0.05:
            insight += f" statistically significant difference ($p = {p_val:.3e} < 0.05$), meaning {faster_team}'s pit crew advantage is consistent and not due to random variation."
        else:
            insight += f" no statistically significant difference ($p = {p_val:.3f} \\ge 0.05$), meaning the observed gap could be attributed to random noise."

        return insight