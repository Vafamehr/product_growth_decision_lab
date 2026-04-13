import json
import os

import pandas as pd

from src.common.paths import ARTIFACTS_DIR
from src.common.schema import (
    CHANNEL_COL,
    CONVERTED_COL,
    EXPERIMENT_GROUP_COL,
    MODEL_TARGET_COL,
    USER_ID_COL,
    USER_TYPE_COL,
)


MODELING_DIR = os.path.join(ARTIFACTS_DIR, "modeling")
DIAGNOSTICS_DIR = os.path.join(ARTIFACTS_DIR, "diagnostics")

MODEL_DATASET_PATH = os.path.join(MODELING_DIR, "conversion_model_dataset.csv")
MODEL_PREDICTIONS_PATH = os.path.join(MODELING_DIR, "conversion_model_predictions.csv")

SCORE_BIN_SUMMARY_PATH = os.path.join(DIAGNOSTICS_DIR, "score_bin_summary.csv")
SEGMENT_SUMMARY_PATH = os.path.join(DIAGNOSTICS_DIR, "segment_summary.csv")
TOP_BUCKET_SUMMARY_PATH = os.path.join(DIAGNOSTICS_DIR, "top_bucket_summary.json")


def load_model_predictions() -> pd.DataFrame:
    if not os.path.exists(MODEL_PREDICTIONS_PATH):
        raise FileNotFoundError(
            f"Missing predictions file: {MODEL_PREDICTIONS_PATH}. "
            "Update train_conversion_model.py to save user_id, actual converted, and predicted probability."
        )

    df = pd.read_csv(MODEL_PREDICTIONS_PATH)

    required_cols = [
        USER_ID_COL,
        MODEL_TARGET_COL,
        "predicted_probability",
        CHANNEL_COL,
        USER_TYPE_COL,
        EXPERIMENT_GROUP_COL,
    ]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Predictions file is missing required columns: {missing_cols}")

    return df


def compute_score_bin_summary(df: pd.DataFrame, n_bins: int = 5) -> pd.DataFrame:
    working_df = df.copy()

    working_df["score_bin"] = pd.qcut(
        working_df["predicted_probability"],
        q=n_bins,
        duplicates="drop",
    )

    summary = (
        working_df.groupby("score_bin", observed=False)
        .agg(
            users=(USER_ID_COL, "count"),
            avg_predicted_probability=("predicted_probability", "mean"),
            actual_conversion_rate=(MODEL_TARGET_COL, "mean"),
        )
        .reset_index()
    )

    summary["lift_vs_overall"] = (
        summary["actual_conversion_rate"] / working_df[MODEL_TARGET_COL].mean()
    )

    summary["score_bin"] = summary["score_bin"].astype(str)

    return summary


def compute_segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    segment_frames = []

    segment_cols = [CHANNEL_COL, USER_TYPE_COL, EXPERIMENT_GROUP_COL]

    for col in segment_cols:
        segment_df = (
            df.groupby(col, observed=False)
            .agg(
                users=(USER_ID_COL, "count"),
                avg_predicted_probability=("predicted_probability", "mean"),
                actual_conversion_rate=(MODEL_TARGET_COL, "mean"),
            )
            .reset_index()
            .rename(columns={col: "segment_value"})
        )

        segment_df["segment_type"] = col
        segment_df["lift_vs_overall"] = (
            segment_df["actual_conversion_rate"] / df[MODEL_TARGET_COL].mean()
        )

        segment_frames.append(segment_df)

    combined = pd.concat(segment_frames, ignore_index=True)
    combined = combined[
        [
            "segment_type",
            "segment_value",
            "users",
            "avg_predicted_probability",
            "actual_conversion_rate",
            "lift_vs_overall",
        ]
    ]

    return combined


def compute_top_bucket_summary(df: pd.DataFrame, top_fraction: float = 0.2) -> dict:
    working_df = df.sort_values("predicted_probability", ascending=False).copy()

    top_n = max(1, int(len(working_df) * top_fraction))

    top_df = working_df.head(top_n)
    overall_rate = working_df[MODEL_TARGET_COL].mean()
    top_rate = top_df[MODEL_TARGET_COL].mean()

    summary = {
        "top_fraction": top_fraction,
        "top_n_users": int(top_n),
        "overall_conversion_rate": float(overall_rate),
        "top_bucket_conversion_rate": float(top_rate),
        "lift_vs_overall": float(top_rate / overall_rate) if overall_rate > 0 else None,
        "avg_predicted_probability_top_bucket": float(top_df["predicted_probability"].mean()),
        "avg_predicted_probability_overall": float(working_df["predicted_probability"].mean()),
    }

    return summary


# ✅ FIXED NAME HERE
def compute_model_diagnostics() -> None:
    os.makedirs(DIAGNOSTICS_DIR, exist_ok=True)

    predictions_df = load_model_predictions()

    score_bin_summary = compute_score_bin_summary(predictions_df, n_bins=5)
    segment_summary = compute_segment_summary(predictions_df)
    top_bucket_summary = compute_top_bucket_summary(predictions_df, top_fraction=0.2)

    score_bin_summary.to_csv(SCORE_BIN_SUMMARY_PATH, index=False)
    segment_summary.to_csv(SEGMENT_SUMMARY_PATH, index=False)

    with open(TOP_BUCKET_SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(top_bucket_summary, f, indent=2)

    print("Model diagnostics completed.")
    print(f"Score bin summary saved to: {SCORE_BIN_SUMMARY_PATH}")
    print(f"Segment summary saved to: {SEGMENT_SUMMARY_PATH}")
    print(f"Top bucket summary saved to: {TOP_BUCKET_SUMMARY_PATH}")

    print("\nTop Bucket Summary")
    print(f"Top Fraction: {top_bucket_summary['top_fraction']:.2f}")
    print(f"Top Users: {top_bucket_summary['top_n_users']}")
    print(f"Overall Conversion Rate: {top_bucket_summary['overall_conversion_rate']:.4f}")
    print(f"Top Bucket Conversion Rate: {top_bucket_summary['top_bucket_conversion_rate']:.4f}")
    print(f"Lift vs Overall: {top_bucket_summary['lift_vs_overall']:.4f}")



if __name__ == "__main__":
    compute_model_diagnostics()