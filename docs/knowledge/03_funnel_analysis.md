# Funnel Analysis — Role in Product Analytics Decision System

## Position in System

Funnel analysis answers:

Why did the experiment result happen?

Pipeline position:

After Experimentation and Statistical Validation, before Decision and Modeling

---

## Objective

Funnel analysis breaks down the user journey into stages.

It helps identify where users drop off and where improvements occur.

---

## Funnel Structure in This System

user to signup to activation to conversion to churn

Important:

- users are generated first  
- signup is not guaranteed  
- each user follows a lifecycle  

---

## Key Metrics

### Signup Rate

signup_rate = signup / total_users

Measures acquisition into the system.

---

### Activation Rate

activation_rate = activation / signup

Measures early engagement after signup.

---

### Conversion After Activation (Critical Metric)

conversion_given_activation = conversion / activation

This isolates the efficiency of converting engaged users.

---

### Overall Conversion Rate

conversion_rate = conversion / total_users

Used in A/B testing, not for diagnosis.

---

## Core Insight

A/B testing tells:

Did conversion increase?

Funnel analysis tells:

Where did it increase?

---

## Example Interpretation

If:

- signup_rate unchanged  
- activation_rate unchanged  
- conversion_given_activation increased  

Then:

The treatment improves conversion after activation, not acquisition.

---

## Why This Matters

Without funnel analysis:

You only know that performance changed.

With funnel analysis:

You understand the mechanism behind the change.

---

## Business Interpretation

Funnel enables statements like:

- improvement is happening after activation  
- acquisition is not affected  
- treatment impacts downstream behavior  

---

## Connection to Decision Layer

Decision uses:

- experiment results  
- statistical validation  

Funnel provides:

explanation and justification for the decision

---

## Connection to Modeling

Funnel tells:

where behavior changes

Modeling tells:

who is likely to convert

Together:

they support targeted strategies

---

## Advanced Concepts (Interview-Level)

### Bottleneck Identification

The weakest stage in the funnel determines overall performance.

Improving that stage gives the highest impact.

---

### Drop-off Analysis

Compare stage-to-stage conversion rates to identify friction points.

---

### Funnel Tradeoffs

Improving one stage may negatively affect another.

Example:

Higher activation may reduce conversion quality.

---

### Funnel vs Absolute Metrics

Absolute metrics hide internal inefficiencies.

Funnel metrics expose them.

---

## Final Takeaway

Funnel analysis is a diagnostic layer.

It explains why performance changed and identifies where improvements occur.