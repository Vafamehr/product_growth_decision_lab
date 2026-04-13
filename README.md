# Product Growth Decision Lab

## Overview

This repository implements a complete product analytics decision system.

It simulates a real-world workflow for:

- analyzing user behavior  
- evaluating A/B experiments  
- diagnosing performance drivers  
- predicting user outcomes  
- supporting business decisions  

This is not a notebook-based analysis project.

It is a structured, reproducible pipeline.

---

## Objective

The system answers the following questions:

- What happened?  
- Did the treatment improve performance?  
- Is the result statistically significant?  
- Why did performance change?  
- For whom did it work?  
- Should we act?  
- Who should we target?  
- Will the effect sustain?  
- What is the final recommendation?  

---

## Pipeline

Run the full system with:

python -m system.run_experiment_pipeline

---

## End-to-End Flow

1. data generation  
2. system metrics  
3. experiment comparison  
4. statistical validation  
5. funnel diagnostics  
6. segmentation  
7. decision logic  
8. conversion modeling  
9. model diagnostics  
10. cohort analysis  
11. final insights  

---

## Repository Structure

src/
  common/
  modules/

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

## Key Components

### Experimentation

- control vs treatment comparison  
- lift calculation  
- statistical testing  

---

### Funnel Analysis

- identifies where behavior changes occur  
- explains performance drivers  

---

### Segmentation

- evaluates performance across user groups  
- supports targeted rollout decisions  

---

### Modeling

- logistic regression for conversion prediction  
- enables user-level ranking  

---

### Cohort Analysis

- measures retention over time  
- evaluates long-term impact  

---

### Decision Layer

- produces ship, rollback, or inconclusive  
- prioritizes business impact  

---

## Key Concepts

- average treatment effect (A/B testing)  
- statistical significance  
- funnel diagnostics  
- heterogeneous user behavior  
- predictive modeling  
- retention analysis  

---

## Design Principles

- deterministic pipeline  
- modular structure  
- artifact-based workflow  
- interpretable outputs  
- decision-focused design  

---

## Final Takeaway

This system connects:

measurement, experimentation, diagnosis, prediction, and decision-making

into a single, coherent product analytics workflow.