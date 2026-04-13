# Product Analytics Decision System — System Overview

## Objective

This system simulates a real-world product analytics workflow.

It is designed to:

- analyze user behavior  
- evaluate product changes using A/B testing  
- diagnose why changes happen  
- predict user outcomes  
- support business decisions  

This is not just a modeling project.

This is a decision system.

---

## Core System Flow

The system follows a structured sequence:

Measure, Compare, Validate, Explain, Segment, Decide, Predict, Target, Evaluate, Synthesize

Mapped to implementation:

| Step | Question | Module |
|------|--------|--------|
| Measure | What happened? | metric_layer |
| Compare | Did treatment help? | experimentation |
| Validate | Is it statistically real? | significance tests |
| Explain | Why did it happen? | funnel_analysis |
| Segment | For whom did it work? | segmentation |
| Decide | Should we act? | decision |
| Predict | Who will convert? | modeling |
| Target | Who should we focus on? | diagnostics |
| Evaluate | Will it sustain? | cohort_analysis |
| Synthesize | What is the final story? | insight_layer |

---

## Key System Idea

A single metric is not enough.

The system combines multiple perspectives:

- Experiment (average treatment effect)  
- Funnel (behavioral mechanism)  
- Segmentation (differences across users)  
- Modeling (prediction and ranking)  
- Cohort (long-term retention)  

---

## Data Structure

The system operates on two core tables.

### users.csv

Contains:

- user_id  
- channel  
- user_type  
- experiment_group  
- signup_day  

---

### events.csv

Contains user lifecycle events:

- signup  
- activation  
- conversion  
- churn  

Each user follows a full lifecycle.

---

## System Components

### Metrics Layer

Computes overall performance:

- conversion rate  
- revenue per user  

Answers:

What is happening at the system level?

---

### Experimentation Layer

Compares:

- control vs treatment  

Outputs:

- lift in conversion and revenue  

Answers:

Did the product change improve performance?

---

### Statistical Layer

Validates results:

- z-test for conversion  
- t-test for revenue  

Answers:

Is the observed difference statistically significant?

---

### Funnel Analysis

Breaks down the user journey:

- signup to activation to conversion  

Answers:

Where did behavior change?

---

### Segmentation Layer

Splits results by:

- channel  
- user_type  

Answers:

For whom does the treatment work?

---

### Decision Layer

Produces final action:

- ship  
- rollback  
- inconclusive  

Logic:

- primarily revenue-driven  
- considers statistical significance  

Answers:

Should we act?

---

### Modeling Layer

Builds a conversion prediction model:

- logistic regression  

Uses:

- channel  
- user_type  
- signup_day  
- experiment_group  

Answers:

Who is likely to convert?

---

### Diagnostics Layer

Evaluates model usefulness:

- top segment performance  
- lift compared to baseline  

Answers:

Is the model useful for targeting?

---

### Cohort Analysis

Tracks retention over time:

- week 1 retention  
- week 4 retention  

Answers:

Do users return after initial interaction?

---

### Insight Layer

Combines all outputs into a final narrative:

- experiment results  
- funnel explanation  
- segment performance  
- model usefulness  
- cohort behavior  

Answers:

What is the complete business story?

---

## Key Distinction

Experiment and modeling serve different purposes.

Experiment measures average impact.

Modeling predicts individual behavior.

---

## Advanced Concept (Interview-Level)

This system estimates average treatment effect.

A more advanced extension is heterogeneous treatment effect.

This leads to uplift modeling, which identifies users who benefit most from treatment.

This is not implemented but is important to understand.

---

## System Strength

This system goes beyond simple metric comparison.

It answers:

- why performance changed  
- where the change happened  
- for whom it is most effective  
- whether it will sustain  
- what action should be taken  

---

## Final Takeaway

A strong product analytics system does not stop at metrics.

It connects measurement, explanation, prediction, and decision into a coherent business narrative.