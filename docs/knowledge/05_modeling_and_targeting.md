# Modeling and Targeting — Role in Product Analytics Decision System

## Position in System

Modeling answers:

Who is likely to convert?

Pipeline position:

After Decision Layer, before Cohort Analysis

---

## Objective

Modeling predicts conversion probability at the user level.

It enables targeted strategies instead of treating all users equally.

---

## Model Used in This System

Logistic Regression

Reason:

- simple and interpretable  
- suitable for binary outcome  
- stable for structured data  

---

## Features Used

- channel  
- user_type  
- signup_day  
- experiment_group  

Important:

No leakage features are used.

Events such as activation or conversion are excluded from inputs.

---

## Output

The model produces:

conversion_probability for each user

This is a continuous score between 0 and 1.

---

## Core Insight

A/B testing provides:

average treatment effect

Modeling provides:

individual conversion likelihood

---

## Ranking vs Classification (Critical Concept)

The model is primarily used for ranking.

Goal is not:

predict exact labels

Goal is:

order users by likelihood of conversion

This enables prioritization.

---

## Diagnostics Used

Top bucket analysis:

- select top 20 percent of users by predicted probability  
- compare their conversion rate to overall conversion  

If top bucket performs significantly better:

model is useful

---

## Business Interpretation

Modeling enables:

- prioritizing high-probability users  
- improving marketing efficiency  
- reducing cost per conversion  

---

## Connection to Segmentation

Segmentation:

coarse grouping

Modeling:

fine-grained ranking within groups

---

## Connection to Decision Layer

Decision answers:

Should we deploy?

Modeling answers:

Where should we apply the treatment?

---

## Advanced Concepts (Interview-Level)

### Calibration

Predicted probabilities should match real-world outcomes.

Poor calibration reduces trust in model outputs.

---

### Feature Importance

Identifies which features influence predictions.

Useful for:

- product insights  
- business interpretation  

---

### Bias and Leakage

Leakage occurs when future information is used in training.

Example:

using activation to predict conversion

This leads to unrealistic performance.

---

### Uplift Modeling (Critical Extension)

Standard model predicts:

probability of conversion

Uplift model predicts:

incremental effect of treatment

Difference:

- standard model answers: who will convert  
- uplift model answers: who will convert because of treatment  

---

### Treatment vs Prediction Confusion

High conversion probability does not imply high treatment effect.

Example:

high-value users may convert anyway

Treatment may be more valuable for marginal users

---

### Model Use in Decision Systems

Model is not used to make the decision.

It is used to support targeting after decision is made.

---

## Limitations

Model does not capture:

- causal relationships  
- treatment effect directly  
- time dynamics  

---

## Final Takeaway

Modeling converts system insight into actionable targeting.

It answers:

Who should we focus on?

But it must be interpreted carefully to avoid confusing prediction with causation.