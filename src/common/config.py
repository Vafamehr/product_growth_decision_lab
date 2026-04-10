from dataclasses import dataclass


@dataclass(frozen=True)
class DataConfig:
    # =========================
    # SIMULATION SIZE / TIME
    # =========================
    n_users: int = 5000
    n_days: int = 90
    random_seed: int = 42

    # =========================
    # ACQUISITION MIX
    # =========================
    organic_share: float = 0.35
    paid_ads_share: float = 0.30
    referral_share: float = 0.20
    partner_share: float = 0.15

    # =========================
    # USER TYPE MIX
    # =========================
    high_value_share: float = 0.20
    medium_value_share: float = 0.50
    low_value_share: float = 0.30

    # =========================
    # FUNNEL STEP BASE RATES
    # These are starting points.
    # Channel and user type effects can adjust them later.
    # =========================
    signup_rate: float = 0.55
    activation_rate: float = 0.65
    conversion_rate: float = 0.30

    # =========================
    # RETENTION / CHURN
    # =========================
    base_day_7_retention: float = 0.40
    base_day_30_retention: float = 0.22
    early_churn_rate: float = 0.25

    # =========================
    # MONETIZATION
    # =========================
    avg_revenue_per_converter: float = 120.0
    revenue_noise_std: float = 20.0

    # =========================
    # EXPERIMENT SETTINGS
    # Small uplift on purpose.
    # We do NOT want cartoonishly obvious results.
    # =========================
    experiment_share: float = 0.50
    treatment_signup_uplift: float = 0.02
    treatment_activation_uplift: float = 0.03
    treatment_conversion_uplift: float = 0.015

    # =========================
    # DIAGNOSTIC / DECISION THRESHOLDS
    # =========================
    min_segment_size: int = 100
    rollout_min_lift: float = 0.01
    rollback_max_retention_drop: float = -0.03


DATA_CONFIG = DataConfig()