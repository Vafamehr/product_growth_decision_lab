from pathlib import Path
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
DATA_DIR = ARTIFACTS_DIR / "data"
OUTPUT_DIR = ARTIFACTS_DIR / "diagnostics"


def compute_segment_performance():
    """
    Segment-level performance:
    - conversion rate by segment
    - lift (treatment vs control)
    
    Segments:
    - channel
    - user_type
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    users = pd.read_csv(DATA_DIR / "users.csv")
    events = pd.read_csv(DATA_DIR / "events.csv")

    # --- conversion flag ---
    conversions = (
        events[events["event_type"] == "conversion"]
        .groupby("user_id")
        .size()
        .reset_index(name="converted")
    )

    conversions["converted"] = 1

    df = users.merge(conversions, on="user_id", how="left")
    df["converted"] = df["converted"].fillna(0)

    results = []

    for segment in ["channel", "user_type"]:

        grouped = (
            df.groupby([segment, "experiment_group"])["converted"]
            .mean()
            .reset_index()
        )

        pivot = grouped.pivot(
            index=segment,
            columns="experiment_group",
            values="converted"
        ).reset_index()

        pivot.columns.name = None

        pivot["lift"] = pivot["treatment"] - pivot["control"]

        pivot["segment"] = segment

        results.append(pivot)

    final_df = pd.concat(results, ignore_index=True)

    output_path = OUTPUT_DIR / "segment_performance.csv"
    final_df.to_csv(output_path, index=False)

    print("\n--- SEGMENT PERFORMANCE ---")
    print(final_df.to_string(index=False))
    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    compute_segment_performance()