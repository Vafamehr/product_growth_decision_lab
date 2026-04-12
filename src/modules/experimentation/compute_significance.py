import math

import numpy as np
import pandas as pd

from src.common.paths import ARTIFACTS_DIR


USERS_PATH = ARTIFACTS_DIR / "data" / "users.csv"
EVENTS_PATH = ARTIFACTS_DIR / "data" / "events.csv"


def compute_significance():
    print("\n===== STATISTICAL SIGNIFICANCE (CONVERSION) =====")

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
    # BUILD USER-LEVEL TABLE
    # =========================
    print("Building user-level conversion table...")

    conversions = (
        df[df["event_type"] == "conversion"]
        .groupby("user_id")
        .size()
        .rename("converted")
    )

    user_df = users.copy()
    user_df = user_df.merge(conversions, on="user_id", how="left")
    user_df["converted"] = user_df["converted"].fillna(0)
    user_df["converted"] = np.where(user_df["converted"] > 0, 1, 0)

    # =========================
    # AGGREGATE BY GROUP
    # =========================
    print("Aggregating by experiment group...")

    summary = user_df.groupby("experiment_group").agg(
        users=("user_id", "count"),
        conversions=("converted", "sum"),
    )

    summary["conversion_rate"] = summary["conversions"] / summary["users"]

    print("\nSummary:")
    print(summary)

    # =========================
    # EXTRACT VALUES
    # =========================
    control = summary.loc["control"]
    treatment = summary.loc["treatment"]

    p1 = control["conversion_rate"]
    p2 = treatment["conversion_rate"]

    n1 = control["users"]
    n2 = treatment["users"]

    x1 = control["conversions"]
    x2 = treatment["conversions"]

    # =========================
    # Z-TEST (TWO-PROPORTION)
    # =========================
    print("\nRunning z-test...")

    p_pool = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * ((1 / n1) + (1 / n2)))
    z = (p2 - p1) / se

    # Two-sided p-value
    p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / np.sqrt(2))))

    lift = (p2 - p1) / p1

    # =========================
    # RESULTS
    # =========================
    print("\n===== RESULTS =====")
    print(f"Control Conversion Rate:    {p1:.4f}")
    print(f"Treatment Conversion Rate:  {p2:.4f}")
    print(f"Lift:                       {lift:.4f}")
    print(f"Z-score:                    {z:.4f}")
    print(f"P-value:                    {p_value:.6f}")

    # =========================
    # DECISION LAYER
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
    compute_significance()