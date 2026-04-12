from src.modules.metric_layer.compute_metrics import compute_metrics
from src.modules.experimentation.compute_experiment_metrics import compute_experiment_metrics
from src.modules.experimentation.compute_significance import compute_significance
from src.modules.experimentation.compute_revenue_significance import compute_revenue_significance
from src.modules.funnel_analysis.compute_experiment_funnel import compute_experiment_funnel
from src.modules.decision.compute_final_decision import compute_final_decision


def run_pipeline():
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

    # 6. FINAL DECISION
    print("\n--- FINAL DECISION ---")
    compute_final_decision(
        conv_p=conv_results["p_value"],
        conv_lift=conv_results["lift"],
        rev_p=rev_results["p_value"],
        rev_lift=rev_results["lift"],
    )


if __name__ == "__main__":
    run_pipeline()