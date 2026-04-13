from src.modules.metric_layer.compute_metrics import compute_metrics
from src.modules.experimentation.compute_experiment_metrics import compute_experiment_metrics
from src.modules.experimentation.compute_significance import compute_significance
from src.modules.experimentation.compute_revenue_significance import compute_revenue_significance
from src.modules.funnel_analysis.compute_experiment_funnel import compute_experiment_funnel
from src.modules.diagnostics.compute_segment_performance import compute_segment_performance
from src.modules.decision.compute_final_decision import compute_final_decision
from src.modules.data_prep.generate_data import generate_data

from src.modules.modeling.train_conversion_model import train_conversion_model
from src.modules.diagnostics.compute_model_diagnostics import compute_model_diagnostics
from src.modules.cohort_analysis.compute_cohort_retention import compute_cohort_retention
from src.modules.insight_layer.generate_final_insights import generate_insights


def run_pipeline():

    # 0. Generate data
    print("\n--- DATA GENERATION ---")
    generate_data()

    print("\n==============================")
    print("PRODUCT GROWTH EXPERIMENT RUN")
    print("==============================")

    # 1. Overall metrics
    print("\n--- SYSTEM METRICS ---")
    compute_metrics()

    # 2. Experiment comparison
    print("\n--- EXPERIMENT METRICS ---")
    compute_experiment_metrics()

    # 3. Conversion significance
    print("\n--- CONVERSION SIGNIFICANCE ---")
    conv_results = compute_significance()

    # 4. Revenue significance
    print("\n--- REVENUE SIGNIFICANCE ---")
    rev_results = compute_revenue_significance()

    # 5. Funnel diagnostics
    print("\n--- FUNNEL ANALYSIS ---")
    compute_experiment_funnel()

    # 6. Segment diagnostics (NEW)
    print("\n--- SEGMENT PERFORMANCE ---")
    compute_segment_performance()

    # 7. Final decision
    print("\n--- FINAL DECISION ---")
    compute_final_decision(
        conv_p=conv_results["p_value"],
        conv_lift=conv_results["lift"],
        rev_p=rev_results["p_value"],
        rev_lift=rev_results["lift"],
    )

    # 8. Modeling
    print("\n--- MODELING ---")
    train_conversion_model()

    # 9. Model diagnostics
    print("\n--- MODEL DIAGNOSTICS ---")
    compute_model_diagnostics()

    # 10. Cohort analysis
    print("\n--- COHORT ANALYSIS ---")
    compute_cohort_retention()

    # 11. Insight layer
    print("\n--- FINAL INSIGHTS ---")
    generate_insights()


if __name__ == "__main__":
    run_pipeline()