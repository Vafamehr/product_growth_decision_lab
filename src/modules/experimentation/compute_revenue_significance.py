import numpy as np
import pandas as pd
from scipy import stats

from src.common.paths import ARTIFACTS_DIR


USERS_PATH = ARTIFACTS_DIR / "data" / "users.csv"
EVENTS_PATH = ARTIFACTS_DIR / "data" / "events.csv"


def compute_revenue_significance():
    print("\n===== REVENUE SIGNIFICANCE =====")

    # =========================
    # LOAD DATA
    # =========================
    print("Loading users and events...")
    users = pd.read_csv(USERS_PATH)
    events = pd.read_csv(EVENTS_PATH)

    # =========================
    # JOIN
    # =========================
    df = events.merge(users, on="user_id", how="left")

    # =========================
    # USER-LEVEL REVENUE
    # =========================
    print("Building user-level revenue...")

    revenue = (
        df[df["event_type"] == "conversion"]
        .groupby("user_id")["revenue"]
        .sum()
        .rename("revenue")
    )

    user_df = users.copy()
    user_df = user_df.merge(revenue, on="user_id", how="left")
    user_df["revenue"] = user_df["revenue"].fillna(0)

    # =========================
    # SPLIT GROUPS
    # =========================
    control = user_df[user_df["experiment_group"] == "control"]["revenue"]
    treatment = user_df[user_df["experiment_group"] == "treatment"]["revenue"]

    # =========================
    # METRICS
    # =========================
    mean_control = control.mean()
    mean_treatment = treatment.mean()

    lift = (mean_treatment - mean_control) / mean_control

    print("\n===== SUMMARY =====")
    print(f"Control Revenue/User:    {mean_control:.4f}")
    print(f"Treatment Revenue/User:  {mean_treatment:.4f}")
    print(f"Lift:                   {lift:.4f}")

    # =========================
    # T-TEST
    # =========================
    print("\nRunning t-test...")

    t_stat, p_value = stats.ttest_ind(treatment, control, equal_var=False)

    print("\n===== RESULTS =====")
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value:     {p_value:.6f}")

    # =========================
    # DECISION
    # =========================
    print("\n===== DECISION =====")

    alpha = 0.05

    if p_value < alpha and lift > 0:
        decision = "SHIP TREATMENT"
    elif p_value < alpha and lift < 0:
        decision = "ROLLBACK TREATMENT"
    else:
        decision = "INCONCLUSIVE — CONTINUE EXPERIMENT"

    print(f"Decision: {decision}")

    # =========================
    # RETURN VALUES
    # =========================
    return {
        "p_value": p_value,
        "lift": lift
    }


if __name__ == "__main__":
    compute_revenue_significance()