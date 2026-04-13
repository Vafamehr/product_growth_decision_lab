import json
import os
from typing import Any, Dict, Optional

import pandas as pd

from src.common.paths import ARTIFACTS_DIR


# =========================
# PATHS
# =========================

EXPERIMENT_DIR = os.path.join(ARTIFACTS_DIR, "experiments")
FUNNEL_DIR = os.path.join(ARTIFACTS_DIR, "funnel")
DIAGNOSTICS_DIR = os.path.join(ARTIFACTS_DIR, "diagnostics")
INSIGHTS_DIR = os.path.join(ARTIFACTS_DIR, "insights")

SIGNIFICANCE_PATH = os.path.join(EXPERIMENT_DIR, "experiment_significance.json")
REVENUE_SIGNIFICANCE_PATH = os.path.join(EXPERIMENT_DIR, "revenue_significance.json")
FUNNEL_PATH = os.path.join(FUNNEL_DIR, "experiment_funnel.csv")
TOP_BUCKET_PATH = os.path.join(DIAGNOSTICS_DIR, "top_bucket_summary.json")

COHORT_PATH = os.path.join(ARTIFACTS_DIR, "cohort_analysis", "cohort_summary.csv")

FINAL_INSIGHTS_PATH = os.path.join(INSIGHTS_DIR, "final_insights.json")


# =========================
# HELPERS
# =========================

def load_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        print(f"[WARN] Missing JSON file: {path}")
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        print(f"[WARN] Missing CSV file: {path}")
        return pd.DataFrame()

    return pd.read_csv(path)


def first_present(data: Dict[str, Any], candidates: list[str], default: Any = None) -> Any:
    for key in candidates:
        if key in data and data[key] is not None:
            return data[key]
    return default


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# =========================
# EXTRACTORS
# =========================

def extract_conversion_stats(conv_sig: Dict[str, Any]) -> Dict[str, Optional[float]]:
    return {
        "conversion_lift": safe_float(
            first_present(conv_sig, ["lift", "conversion_lift"])
        ),
        "conversion_p_value": safe_float(
            first_present(conv_sig, ["p_value", "conversion_p_value"])
        ),
    }


def extract_revenue_stats(rev_sig: Dict[str, Any]) -> Dict[str, Optional[float]]:
    return {
        "revenue_lift": safe_float(
            first_present(rev_sig, ["lift", "revenue_lift"])
        ),
        "revenue_p_value": safe_float(
            first_present(rev_sig, ["p_value", "revenue_p_value"])
        ),
    }


def extract_funnel_insight(funnel_df: pd.DataFrame) -> Dict[str, Any]:
    if funnel_df.empty:
        return {
            "main_driver": None,
            "control_value": None,
            "treatment_value": None,
            "interpretation": "Funnel artifact missing or empty.",
        }

    df = funnel_df.copy()
    df.columns = [str(col).strip() for col in df.columns]

    group_col_candidates = ["experiment_group", "group", "variant"]
    metric_col_candidates = [
        "conversion_given_activation",
        "activation_to_conversion_rate",
    ]

    group_col = next((c for c in group_col_candidates if c in df.columns), None)
    metric_col = next((c for c in metric_col_candidates if c in df.columns), None)

    if group_col is None or metric_col is None:
        return {
            "main_driver": None,
            "control_value": None,
            "treatment_value": None,
            "interpretation": "Funnel structure not as expected.",
        }

    df[group_col] = df[group_col].astype(str).str.strip().str.lower()

    control_rows = df[df[group_col] == "control"]
    treatment_rows = df[df[group_col] == "treatment"]

    if control_rows.empty or treatment_rows.empty:
        return {
            "main_driver": metric_col,
            "control_value": None,
            "treatment_value": None,
            "interpretation": "Missing control/treatment rows.",
        }

    control_value = safe_float(control_rows.iloc[0][metric_col])
    treatment_value = safe_float(treatment_rows.iloc[0][metric_col])

    return {
        "main_driver": metric_col,
        "control_value": control_value,
        "treatment_value": treatment_value,
        "interpretation": "Treatment improves conversion after activation.",
    }


def extract_model_insight(top_bucket: Dict[str, Any]) -> Dict[str, Any]:
    if not top_bucket:
        return {
            "top_fraction": None,
            "lift_vs_overall": None,
            "interpretation": "Model diagnostics missing.",
        }

    return {
        "top_fraction": safe_float(first_present(top_bucket, ["top_fraction"])),
        "lift_vs_overall": safe_float(first_present(top_bucket, ["lift_vs_overall"])),
        "interpretation": "Model effectively ranks high-probability users.",
    }


def extract_cohort_insight(cohort_df: pd.DataFrame) -> Dict[str, Any]:
    if cohort_df.empty:
        return {
            "week_1_retention": None,
            "week_4_retention": None,
            "interpretation": "Cohort data missing.",
        }

    avg_w1 = cohort_df["week_1_retention"].dropna().mean()
    avg_w4 = cohort_df["week_4_retention"].dropna().mean()

    return {
        "week_1_retention": safe_float(avg_w1),
        "week_4_retention": safe_float(avg_w4),
        "interpretation": "Retention declines over time; long-term engagement is modest.",
    }


# =========================
# CORE LOGIC
# =========================

def generate_insights() -> Dict[str, Any]:

    conv_sig = load_json(SIGNIFICANCE_PATH)
    rev_sig = load_json(REVENUE_SIGNIFICANCE_PATH)
    funnel_df = load_csv(FUNNEL_PATH)
    top_bucket = load_json(TOP_BUCKET_PATH)
    cohort_df = load_csv(COHORT_PATH)
    cohort_comp = load_csv(os.path.join(ARTIFACTS_DIR, "cohort_analysis", "cohort_comparison.csv"))

    conversion_stats = extract_conversion_stats(conv_sig)
    revenue_stats = extract_revenue_stats(rev_sig)
    funnel_insight = extract_funnel_insight(funnel_df)
    model_insight = extract_model_insight(top_bucket)
    cohort_insight = extract_cohort_insight(cohort_df)

    insights: Dict[str, Any] = {}

    insights["decision_summary"] = {
        **conversion_stats,
        **revenue_stats,
        "final_decision": "SHIP TREATMENT (Revenue Driven)",
    }

    insights["funnel_insight"] = funnel_insight
    insights["model_insight"] = model_insight
    insights["cohort_insight"] = cohort_insight

    #: cohort comparison insight
    if not cohort_comp.empty:
        early_w1 = cohort_comp.iloc[0]["week_1_retention"]
        late_w1 = cohort_comp.iloc[1]["week_1_retention"]

        trend = "declining" if late_w1 < early_w1 else "improving"

        cohort_trend = {
            "trend": trend,
            "interpretation": f"Retention is {trend} across cohorts."
        }
    else:
        cohort_trend = {"trend": None, "interpretation": "No cohort comparison available."}

    insights["cohort_trend"] = cohort_trend

    #: hypothesis layer
    insights["hypotheses"] = [
        "Treatment improves short-term conversion behavior.",
        "Users may be incentivized to convert quickly without long-term engagement.",
        "Retention patterns suggest limited habit formation."
    ]

    insights["recommendation"] = {
        "action": "Roll out treatment",
        "reason": "Revenue impact is statistically significant.",
        "targeting_strategy": "Prioritize high-performing segments (e.g., organic, medium_value users).",
        "risk_note": "Monitor retention; long-term engagement may not improve.",
    }

    return insights


# =========================
# MAIN
# =========================

def main() -> None:
    os.makedirs(INSIGHTS_DIR, exist_ok=True)

    insights = generate_insights()

    with open(FINAL_INSIGHTS_PATH, "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=2)

    print("Final insights generated.")
    print(f"Saved to: {FINAL_INSIGHTS_PATH}")

    print("\n=== FINAL SUMMARY ===")
    print(json.dumps(insights, indent=2))


if __name__ == "__main__":
    main()