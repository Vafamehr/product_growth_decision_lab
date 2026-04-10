import pandas as pd

from src.common.paths import DATA_DIR, METRICS_DIR, ensure_directories


def compute_metrics():
    ensure_directories()

    users = pd.read_csv(DATA_DIR / "users.csv")
    events = pd.read_csv(DATA_DIR / "events.csv")

    # ---------------------
    # BASIC COUNTS
    # ---------------------
    total_users = users["user_id"].nunique()

    signup_users = events[events["event_type"] == "signup"]["user_id"].nunique()
    activated_users = events[events["event_type"] == "activation"]["user_id"].nunique()
    converted_users = events[events["event_type"] == "conversion"]["user_id"].nunique()

    # ---------------------
    # FUNNEL RATES
    # ---------------------
    signup_rate = signup_users / total_users if total_users else 0
    activation_rate = activated_users / signup_users if signup_users else 0
    conversion_rate = converted_users / activated_users if activated_users else 0

    # ---------------------
    # REVENUE
    # ---------------------
    total_revenue = events.loc[
        events["event_type"] == "conversion", "revenue"
    ].sum()

    avg_revenue_per_user = total_revenue / total_users if total_users else 0

    # ---------------------
    # METRICS TABLE
    # ---------------------
    metrics = pd.DataFrame({
        "metric": [
            "total_users",
            "signup_users",
            "activated_users",
            "converted_users",
            "signup_rate",
            "activation_rate",
            "conversion_rate",
            "total_revenue",
            "avg_revenue_per_user",
        ],
        "value": [
            total_users,
            signup_users,
            activated_users,
            converted_users,
            signup_rate,
            activation_rate,
            conversion_rate,
            total_revenue,
            avg_revenue_per_user,
        ],
    })

    # ---------------------
    # SAVE
    # ---------------------
    metrics.to_csv(METRICS_DIR / "overall_metrics.csv", index=False)

    print("\n===== OVERALL METRICS =====")
    print(metrics)


if __name__ == "__main__":
    compute_metrics()