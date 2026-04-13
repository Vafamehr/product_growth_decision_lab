from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
DATA_DIR = ARTIFACTS_DIR / "data"
OUTPUT_DIR = ARTIFACTS_DIR / "cohort_analysis"


def _load_events() -> pd.DataFrame:
    events_path = DATA_DIR / "events.csv"

    if not events_path.exists():
        raise FileNotFoundError(f"Missing required file: {events_path}")

    events = pd.read_csv(events_path)

    required_cols = ["user_id", "day", "event_type"]
    missing = [col for col in required_cols if col not in events.columns]
    if missing:
        raise ValueError(f"events.csv is missing required columns: {missing}")

    events = events[required_cols].copy()
    return events


def compute_cohort_retention() -> None:

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    events = _load_events()

    signup_events = (
        events[events["event_type"] == "signup"]
        .sort_values(["user_id", "day"])
        .drop_duplicates(subset=["user_id"], keep="first")
        .rename(columns={"day": "signup_day"})
        [["user_id", "signup_day"]]
        .copy()
    )

    signup_events["cohort_day"] = signup_events["signup_day"]

    activity_events = events[events["event_type"] != "signup"].copy()

    cohort_size = (
        signup_events.groupby("cohort_day", as_index=False)["user_id"]
        .nunique()
        .rename(columns={"user_id": "cohort_size"})
    )

    week_zero = cohort_size.copy()
    week_zero["cohort_week"] = 0
    week_zero["retained_users"] = week_zero["cohort_size"]

    cohort_activity = activity_events.merge(signup_events, on="user_id", how="inner")
    cohort_activity = cohort_activity[cohort_activity["day"] >= cohort_activity["signup_day"]].copy()

    cohort_activity["days_since_signup"] = cohort_activity["day"] - cohort_activity["signup_day"]
    cohort_activity["cohort_week"] = (cohort_activity["days_since_signup"] // 7).astype(int)

    retained = (
        cohort_activity.groupby(["cohort_day", "cohort_week"], as_index=False)["user_id"]
        .nunique()
        .rename(columns={"user_id": "retained_users"})
    )

    cohort_retention_long = pd.concat(
        [
            week_zero[["cohort_day", "cohort_week", "retained_users"]],
            retained,
        ],
        ignore_index=True,
    )

    cohort_retention_long = (
        cohort_retention_long.drop_duplicates(subset=["cohort_day", "cohort_week"], keep="first")
        .merge(cohort_size, on="cohort_day", how="left")
        .sort_values(["cohort_day", "cohort_week"])
        .reset_index(drop=True)
    )

    cohort_retention_long["retention_rate"] = (
        cohort_retention_long["retained_users"] / cohort_retention_long["cohort_size"]
    ).round(4)

    cohort_summary = (
        cohort_retention_long[cohort_retention_long["cohort_week"].isin([1, 4])]
        .pivot(index="cohort_day", columns="cohort_week", values="retention_rate")
        .reset_index()
        .rename(columns={1: "week_1_retention", 4: "week_4_retention"})
    )

    #cohort comparison
    midpoint = cohort_summary["cohort_day"].median()

    early = cohort_summary[cohort_summary["cohort_day"] <= midpoint]
    late = cohort_summary[cohort_summary["cohort_day"] > midpoint]

    comparison = pd.DataFrame({
        "group": ["early_cohorts", "late_cohorts"],
        "week_1_retention": [
            early["week_1_retention"].mean(),
            late["week_1_retention"].mean()
        ],
        "week_4_retention": [
            early["week_4_retention"].mean(),
            late["week_4_retention"].mean()
        ]
    })

    cohort_summary.to_csv(OUTPUT_DIR / "cohort_summary.csv", index=False)
    comparison.to_csv(OUTPUT_DIR / "cohort_comparison.csv", index=False)

    print("\n--- COHORT SUMMARY (HEAD) ---")
    print(cohort_summary.head(5).to_string(index=False))

    print("\n--- COHORT COMPARISON ---")
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    compute_cohort_retention()