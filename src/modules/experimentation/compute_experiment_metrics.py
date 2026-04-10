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
    # RATES (ABSOLUTE)
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
    # BUILD METRIC TABLE
    # =========================
    print("Building metric table...")

    metric_map = {
        "signup_rate": signup_rate,
        "activation_rate": activation_rate,
        "conversion_rate": conversion_rate,
        "avg_revenue_per_user": revenue_per_user,
    }

    metrics = []

    for group in total_users.index:
        for metric_name, series in metric_map.items():
            metrics.append({
                "experiment_group": group,
                "metric": metric_name,
                "value": series.get(group, 0)
            })

    metrics_df = pd.DataFrame(metrics)

    # =========================
    # LIFT CALCULATION
    # =========================
    print("Computing lift (treatment vs control)...")

    pivot = metrics_df.pivot(index="metric", columns="experiment_group", values="value")

    # Ensure both groups exist
    if "control" in pivot.columns and "treatment" in pivot.columns:
        pivot["lift"] = (pivot["treatment"] - pivot["control"]) / pivot["control"]
    else:
        print("Warning: Missing control or treatment group for lift calculation")
        pivot["lift"] = None

    lift_df = pivot.reset_index()[["metric", "lift"]]

    # =========================
    # SAVE
    # =========================
    print(f"Saving results to {OUTPUT_PATH}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save both tables (merged for simplicity)
    final_df = metrics_df.merge(lift_df, on="metric", how="left")

    final_df.to_csv(OUTPUT_PATH, index=False)

    # =========================
    # PRINT
    # =========================
    print("\n===== RESULTS =====")
    print(final_df.sort_values(["metric", "experiment_group"]))


if __name__ == "__main__":
    compute_experiment_metrics()