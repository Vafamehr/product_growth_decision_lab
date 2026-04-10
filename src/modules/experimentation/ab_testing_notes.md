# A/B Testing — Key Concepts & Interview Notes

## 1. Measure → Compare → Validate → Decide

* Measure: compute product metrics (conversion, revenue)
* Compare: control vs treatment, compute lift
* Validate: statistical significance (z-test, p-value)
* Decide: ship / rollback / continue experiment

---

## 2. Absolute vs Funnel Rates

**Absolute (Experiment)**

* conversion_rate = conversions / total_users
* Used for A/B comparison

**Funnel (Diagnostic)**

* conversion_given_activation = conversions / activations
* Used for understanding step efficiency

---

## 3. Lift Definition

Lift measures relative improvement of treatment over control:

lift = (treatment - control) / control

Important:

* NOT percentage points
* Relative % increase

---

## 4. Standard Error (Two Proportions)

SE = sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))

Where:

* n1, n2 = sample sizes
* p_pool = pooled conversion rate

---

## 5. Why Use Pooled Probability

Under the null hypothesis:

H0: p1 = p2

Both groups are assumed to come from the same population.

So we estimate one shared probability:

p_pool = (x1 + x2) / (n1 + n2)

This ensures:

* correct variance estimate
* consistency with hypothesis

---

## 6. Interpretation

Example:

control = 0.095
treatment = 0.111

Absolute increase:
+0.016 (~1.6 percentage points)

Relative lift:
+17%

Correct phrasing:
"Treatment increased conversion by 17%"

---

## 7. Modeling Note (Important)

If signup_rate < 1.0:

* Users include pre-signup population
* Funnel becomes: user → signup → activation → conversion

If signup_rate = 1.0:

* Users are already signed-up customers
* Funnel starts at activation

This is a modeling choice.

---

## 8. Key Insight

A/B testing does NOT require ML.

It is:

* statistical comparison
* based on observed data

ML comes later for:

* prediction
* targeting
* personalization
