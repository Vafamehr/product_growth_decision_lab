import pandas as pd
from pathlib import Path

from src.common.paths import ARTIFACTS_DIR


USERS_PATH = ARTIFACTS_DIR / "data" / "users.csv"
EVENTS_PATH = ARTIFACTS_DIR / "data" / "events.csv"

OUTPUT_DIR = ARTIFACTS_DIR / "experiments"
OUTPUT_PATH = OUTPUT_DIR / "experiment_metrics.csv"


def compute_experiment_metrics():
    print("\n===== EXPERIMENT METRICS (A/B) =====")

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
    # BASE COUNTS
    # =========================
    print("Computing base counts...")

    total_users = users.groupby("experiment_group")["user_id"].nunique()

    signup_users = (
        df[df["event_type"] == "signup"]
        .groupby("experiment_group")["user_id"]
        .nunique()
    )

    activation_users = (
        df[df["event_type"] == "activation"]
        .groupby("experiment_group")["user_id"]
        .nunique()
    )

    conversion_users = (
        df[df["event_type"] == "conversion"]
        .groupby("experiment_group")["user_id"]
        .nunique()
    )

    # =========================
    # RATES
    # =========================
    print("Computing rates...")

    signup_rate = signup_users / total_users
    activation_rate = activation_users / total_users
    conversion_rate = conversion_users / total_users

    # =========================
    # REVENUE
    # =========================
    print("Computing revenue metrics...")

    revenue_per_user = (
        df[df["event_type"] == "conversion"]
        .groupby("experiment_group")["revenue"]
        .sum()
        / total_users
    )

    # =========================
    # BUILD OUTPUT TABLE
    # =========================
    print("Building output table...")

    metrics = []

    for group in total_users.index:
        metrics.extend([
            {"experiment_group": group, "metric": "signup_rate", "value": signup_rate.get(group, 0)},
            {"experiment_group": group, "metric": "activation_rate", "value": activation_rate.get(group, 0)},
            {"experiment_group": group, "metric": "conversion_rate", "value": conversion_rate.get(group, 0)},
            {"experiment_group": group, "metric": "avg_revenue_per_user", "value": revenue_per_user.get(group, 0)},
        ])

    metrics_df = pd.DataFrame(metrics)

    # =========================
    # SAVE
    # =========================
    print(f"Saving results to {OUTPUT_PATH}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(OUTPUT_PATH, index=False)

    # =========================
    # PRINT
    # =========================
    print("\n===== RESULTS =====")
    print(metrics_df.sort_values(["experiment_group", "metric"]))


if __name__ == "__main__":
    compute_experiment_metrics()