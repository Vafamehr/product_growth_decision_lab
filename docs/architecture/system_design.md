# Product Analytics Decision System — Architecture

## Overview

This repository is a deterministic, modular product analytics system.

It transforms simulated user and event data into:

- experiment evaluation  
- behavioral diagnostics  
- user-level prediction  
- retention analysis  
- final business recommendation  

This is not a notebook-style analysis project.

It is a structured pipeline.

---

## Architectural Goal

The system is designed to answer a sequence of business questions:

1. What happened?  
2. Did the treatment help?  
3. Is the difference statistically meaningful?  
4. Why did performance change?  
5. For whom did it work?  
6. Should we act?  
7. Who should we target?  
8. Will the effect sustain?  
9. What is the final business story?  

---

## Repository Structure

product_growth_decision_lab/

src/
  common/
    config.py
    paths.py
    schema.py

  modules/
    data_prep/
      generate_data.py

    metric_layer/
      compute_metrics.py

    experimentation/
      compute_experiment_metrics.py
      compute_significance.py
      compute_revenue_significance.py

    funnel_analysis/
      compute_experiment_funnel.py

    diagnostics/
      compute_segment_performance.py
      compute_model_diagnostics.py

    decision/
      compute_final_decision.py

    modeling/
      train_conversion_model.py

    cohort_analysis/
      compute_cohort_retention.py

    insight_layer/
      generate_final_insights.py

system/
  run_experiment_pipeline.py

artifacts/
  data/
  metrics/
  experiments/
  funnel/
  diagnostics/
  decision/
  modeling/
  cohort_analysis/
  insights/

docs/
  knowledge/
  architecture/

---

## Execution Model

The system runs through a single command:

python -m system.run_experiment_pipeline

This executes the full pipeline from data generation to final insights.

The pipeline is:

- deterministic  
- reproducible  
- script-based  
- independent of notebooks  

---

## End-to-End Pipeline Flow

1. data generation  
2. system metrics  
3. experiment metrics  
4. conversion significance  
5. revenue significance  
6. funnel analysis  
7. segment performance  
8. final decision  
9. conversion modeling  
10. model diagnostics  
11. cohort analysis  
12. final insights  

---

## Module Responsibilities

Data Prep  
Generates synthetic users and events data  
Outputs artifacts/data/users.csv and events.csv  

Metric Layer  
Computes overall system metrics such as conversion rate and revenue per user  

Experimentation Layer  
Compares control vs treatment and computes lift and statistical significance  

Funnel Analysis  
Breaks down user journey and identifies where behavioral changes occur  

Diagnostics Layer  
Evaluates segment-level performance and model usefulness  

Decision Layer  
Produces final business action: ship, rollback, or inconclusive  

Modeling Layer  
Builds a conversion prediction model using user features  

Cohort Analysis  
Tracks retention over time and compares cohorts  

Insight Layer  
Combines all outputs into a final business narrative  

---

## Data Flow Pattern

Each module:

1. reads input artifacts  
2. performs a focused transformation  
3. writes output artifacts  

Artifacts are stored as CSV or JSON files.

This creates loose coupling between modules.

---

## Design Principles

Deterministic  
Same inputs produce same outputs  

Modular  
Each module has a single responsibility  

Interpretable  
Outputs are explainable and readable  

Decision-Focused  
The system is organized around business questions  

Simple  
Avoid unnecessary complexity  

---

## Architectural Logic

Layer 1: Measurement  
Data prep and metrics  

Layer 2: Causal Comparison  
Experimentation and statistical validation  

Layer 3: Behavioral Diagnosis  
Funnel and segmentation  

Layer 4: Action  
Decision layer  

Layer 5: Prediction  
Modeling and diagnostics  

Layer 6: Long-Term Validation  
Cohort analysis  

Layer 7: Synthesis  
Insight layer  

---

## System Strength

This system integrates:

- experiment evaluation  
- funnel diagnosis  
- segmentation  
- prediction  
- retention  
- decision logic  

It reflects a real-world analytics workflow rather than a single model.

---

## Limitations

This is a batch-style system.

It does not include:

- real-time processing  
- streaming pipelines  
- production APIs  
- dashboards  

---

## Advanced Extensions

Possible future extensions include:

- uplift modeling for treatment-aware targeting  
- heterogeneous treatment effect modeling  
- survival analysis for retention  
- guardrail metrics  
- partial rollout strategies  

---

## Final Takeaway

Each module answers one business question and passes results forward.

The system moves from raw data to a final decision in a structured, explainable way.