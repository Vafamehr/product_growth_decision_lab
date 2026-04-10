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