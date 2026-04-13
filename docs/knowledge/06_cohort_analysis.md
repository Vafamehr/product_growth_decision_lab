# Cohort Analysis — Role in Product Analytics Decision System

## Position in System

Cohort analysis answers:

Will the observed improvement sustain over time?

Pipeline position:

After Modeling and Diagnostics, before Final Insight Layer

---

## Objective

Cohort analysis tracks user behavior over time.

It measures retention rather than immediate outcomes.

---

## Cohort Definition in This System

A cohort is defined by:

signup_day

Users who sign up on the same day belong to the same cohort.

---

## Retention Definition

A user is considered retained if they perform any activity after signup.

Retention is measured at different time intervals.

---

## Key Metrics

### Week 1 Retention

Percentage of users active within the first week after signup.

---

### Week 4 Retention

Percentage of users active in later periods.

---

## Core Insight

A/B testing measures:

short-term impact

Cohort analysis measures:

long-term engagement

---

## Example Interpretation

If:

- conversion increases  
- retention remains low  

Then:

Users convert but do not continue engaging

---

## Cohort Comparison

The system compares:

early cohorts vs late cohorts

Purpose:

detect trends over time

---

## Trend Interpretation

### Declining Retention

- novelty effect  
- weaker later users  
- short-term incentives dominate  

---

### Improving Retention

- product experience improving  
- stronger engagement over time  

---

## Why This Matters

Without cohort analysis:

Decisions are based only on immediate results

With cohort analysis:

Long-term impact is considered

---

## Connection to Decision Layer

Decision uses:

short-term metrics

Cohort provides:

risk assessment for long-term performance

---

## Connection to Modeling

Model predicts:

who converts

Cohort evaluates:

whether those users stay

---

## Advanced Concepts (Interview-Level)

### Retention Curve

Retention plotted over time gives deeper insight than single points.

---

### Survival Analysis

Models time until churn or conversion.

Used for more advanced retention modeling.

---

### Cohort Bias

Later cohorts may differ in quality from earlier cohorts.

Must be considered in interpretation.

---

### Tradeoff Between Conversion and Retention

Some treatments increase conversion but reduce long-term engagement.

---

## Limitations

Cohort analysis requires sufficient time window.

Recent cohorts may have incomplete data.

---

## Final Takeaway

Cohort analysis adds a long-term perspective.

It answers:

Will the improvement last?