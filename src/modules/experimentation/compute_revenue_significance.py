import json
import os

import numpy as np
import pandas as pd

from src.common.paths import ARTIFACTS_DIR


USERS_PATH = ARTIFACTS_DIR / "data" / "users.csv"
EVENTS_PATH = ARTIFACTS_DIR / "data" / "events.csv"

OUTPUT_DIR = ARTIFACTS_DIR / "experiments"
OUTPUT_PATH = OUTPUT_DIR / "revenue_significance.json"


def compute_revenue_significance():
    print("\n===== STATISTICAL SIGNIFICANCE (REVENUE) =====")

    # =========================
    # LOAD DATA
    # =========================
    print("Loading users and events...")
    users = pd.read_csv(USERS_PATH)
    events = pd.read_csv(EVENTS_PATH)

    # =========================
    # JOIN
    # =========================
    print("Joining users with events...")
    df = events.merge(users, on="user_id", how="left")

    # =========================
    # DETECT REVENUE COLUMN
    # =========================
    print("Detecting revenue column...")

    possible_cols = ["amount", "revenue", "value"]
    revenue_col = None

    for col in possible_cols:
        if col in df.columns:
            revenue_col = col
            break

    if revenue_col is None:
        raise ValueError(
            f"No revenue column found. Available columns: {list(df.columns)}"
        )

    print(f"Using revenue column: {revenue_col}")

    # =========================
    # BUILD USER-LEVEL REVENUE
    # =========================
    print("Building user-level revenue...")

    revenue_df = (
        df[df["event_type"] == "conversion"]
        .groupby("user_id")[revenue_col]
        .sum()
        .rename("revenue")
    )

    user_df = users.copy()
    user_df = user_df.merge(revenue_df, on="user_id", how="left")
    user_df["revenue"] = user_df["revenue"].fillna(0)

    # =========================
    # SPLIT GROUPS
    # =========================
    control = user_df[user_df["experiment_group"] == "control"]["revenue"]
    treatment = user_df[user_df["experiment_group"] == "treatment"]["revenue"]

    # =========================
    # MEANS
    # =========================
    mean_control = control.mean()
    mean_treatment = treatment.mean()

    lift = (mean_treatment - mean_control) / mean_control if mean_control != 0 else 0

    # =========================
    # T-TEST (MANUAL)
    # =========================
    print("Running t-test...")

    var_control = control.var(ddof=1)
    var_treatment = treatment.var(ddof=1)

    n1 = len(control)
    n2 = len(treatment)

    se = np.sqrt((var_control / n1) + (var_treatment / n2))
    t_stat = (mean_treatment - mean_control) / se if se != 0 else 0

    # approximate p-value (normal approximation)
    from math import erf, sqrt

    p_value = 2 * (1 - 0.5 * (1 + erf(abs(t_stat) / sqrt(2))))

    # =========================
    # RESULTS
    # =========================
    print("\n===== RESULTS =====")
    print(f"Control Revenue:    {mean_control:.4f}")
    print(f"Treatment Revenue:  {mean_treatment:.4f}")
    print(f"Lift:               {lift:.4f}")
    print(f"T-stat:             {t_stat:.4f}")
    print(f"P-value:            {p_value:.6f}")

    result = {
        "p_value": float(p_value),
        "lift": float(lift),
        "t_stat": float(t_stat),
        "control_mean": float(mean_control),
        "treatment_mean": float(mean_treatment),
    }

    # =========================
    # SAVE OUTPUT
    # =========================
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"\nSaved to: {OUTPUT_PATH}")

    return result


if __name__ == "__main__":
    compute_revenue_significance()