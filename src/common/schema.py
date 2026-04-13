from dataclasses import dataclass
from typing import Optional


# =========================
# USER ENTITY
# =========================
@dataclass
class User:
    user_id: int
    signup_day: int

    # Acquisition
    channel: str  # organic, paid_ads, referral, partner

    # User quality / value
    user_type: str  # high_value, medium_value, low_value

    # Experiment
    experiment_group: str  # control or treatment


# =========================
# EVENT ENTITY
# =========================
@dataclass
class Event:
    user_id: int
    day: int

    event_type: str  # signup, activation, conversion, churn

    # Optional fields
    revenue: Optional[float] = None


# =========================
# EXPERIMENT RESULT ENTITY
# =========================
@dataclass
class ExperimentResult:
    metric_name: str

    control_value: float
    treatment_value: float

    lift: float

    # Optional statistical fields (filled later)
    p_value: Optional[float] = None
    standard_error: Optional[float] = None


# =========================
# CANONICAL COLUMN NAMES
# =========================

# Shared keys
USER_ID_COL = "user_id"
DAY_COL = "day"

# User table columns
SIGNUP_DAY_COL = "signup_day"
CHANNEL_COL = "channel"
USER_TYPE_COL = "user_type"
EXPERIMENT_GROUP_COL = "experiment_group"

# Event table columns
EVENT_TYPE_COL = "event_type"
REVENUE_COL = "revenue"

# Event values
SIGNUP_EVENT = "signup"
ACTIVATION_EVENT = "activation"
CONVERSION_EVENT = "conversion"
CHURN_EVENT = "churn"

# Experiment values
CONTROL_GROUP = "control"
TREATMENT_GROUP = "treatment"


# =========================
# MODELING COLUMN NAMES
# =========================
ACTIVATED_COL = "activated"
CONVERTED_COL = "converted"
CHURNED_COL = "churned"
EVENT_COUNT_COL = "event_count"
TOTAL_REVENUE_COL = "total_revenue"

# Optional future-friendly names
CHANNEL_ORGANIC_COL = "channel_organic"
CHANNEL_PAID_ADS_COL = "channel_paid_ads"
CHANNEL_REFERRAL_COL = "channel_referral"
CHANNEL_PARTNER_COL = "channel_partner"

USER_TYPE_HIGH_VALUE_COL = "user_type_high_value"
USER_TYPE_MEDIUM_VALUE_COL = "user_type_medium_value"
USER_TYPE_LOW_VALUE_COL = "user_type_low_value"

EXPERIMENT_TREATMENT_COL = "experiment_treatment"


# =========================
# MODEL TARGET + FEATURES
# =========================
MODEL_TARGET_COL = CONVERTED_COL

BASE_MODEL_FEATURES = [
    ACTIVATED_COL,
    CHURNED_COL,
    EVENT_COUNT_COL,
]

EXTENDED_MODEL_FEATURES = [
    ACTIVATED_COL,
    CHURNED_COL,
    EVENT_COUNT_COL,
    CHANNEL_COL,
    USER_TYPE_COL,
    EXPERIMENT_GROUP_COL,
]