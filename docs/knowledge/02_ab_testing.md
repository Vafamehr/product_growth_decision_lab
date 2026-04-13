# A/B Testing — Role in Product Analytics Decision System

## Position in System

A/B testing answers:

Did the treatment improve performance?

Pipeline position:

Metrics, then Experimentation, then Statistical Validation, then Decision

---

## Objective

A/B testing compares two groups:

- control group (baseline experience)  
- treatment group (new product change)  

The goal is to measure the impact of the change on business metrics.

---

## Key Metrics

### Conversion Rate

conversion_rate = conversions / total_users

Primary behavioral metric.

---

### Revenue per User

revenue_per_user = total_revenue / total_users

Primary business metric used for decision-making in this system.

---

## Lift Definition

Lift measures relative improvement of treatment over control.

lift = (treatment - control) / control

Important:

- lift is relative, not absolute  
- do not confuse with percentage point difference  

---

## Statistical Validation

Observed differences are not sufficient.

We must validate whether the difference is statistically meaningful.

---

### Conversion Test (z-test)

Used for proportions.

Inputs:

- conversion rates  
- sample sizes  

Output:

- p-value  

---

### Revenue Test (t-test)

Used for continuous variables.

Inputs:

- revenue distributions  

Output:

- p-value  

---

## Interpretation of p-value

p-value represents the probability of observing the result if no real effect exists.

Typical threshold:

- p < 0.05 indicates statistical significance  

Important:

- statistical significance does not imply business importance  
- large samples can make small effects significant  

---

## Sample Size and Power (Critical Concept)

Reliable experiments require sufficient sample size.

Small samples lead to:

- unstable estimates  
- high variance  
- misleading conclusions  

Power refers to the probability of detecting a real effect.

Low power leads to false negatives.

---

## Randomization and Validity

A/B testing assumes:

- users are randomly assigned  
- groups are comparable  

Key checks:

- similar group sizes  
- similar baseline characteristics  

Violations lead to biased results.

---

## Key Limitation

A/B testing measures:

average treatment effect

It does not tell:

- why the change worked  
- where the change occurred  
- for whom the change worked  

---

## Connection to Other Modules

Funnel analysis explains:

where the improvement occurred

Segmentation explains:

which users responded differently

Modeling predicts:

which users are likely to convert

---

## Advanced Concepts (Interview-Level)

### Heterogeneous Treatment Effect

Different users respond differently to the same treatment.

A/B testing averages over all users and hides this variation.

---

### Uplift Modeling

Predicts the incremental impact of treatment at the user level.

Difference from standard modeling:

- standard model predicts conversion  
- uplift model predicts treatment effect  

---

### Simpson’s Paradox

Aggregate results can hide opposite trends within segments.

Example:

Treatment looks positive overall  
But negative in a key segment  

---

### Novelty Effect

Users may respond strongly at first, then behavior declines over time.

This requires cohort analysis to detect.

---

### Interference

Users may influence each other.

This violates independence assumptions.

Example:

social or network effects

---

### Carryover Effects

Previous exposure to treatment may influence future behavior.

Important in repeated experiments.

---

## Experiment Pitfalls

- insufficient sample size  
- imbalance between groups  
- leakage between control and treatment  
- external events affecting behavior  
- misinterpretation of p-values  

---

## Business Interpretation

A/B testing provides the foundation for decision-making.

However:

- results must be interpreted in context  
- statistical significance must be paired with business impact  

---

## Final Takeaway

A/B testing answers:

Did the change work on average?

It is necessary but not sufficient.

It must be combined with diagnostics, segmentation, and modeling to form a complete decision.