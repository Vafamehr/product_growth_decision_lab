import numpy as np
import pandas as pd

from src.common.config import DATA_CONFIG
from src.common.paths import DATA_DIR, ensure_directories


# =========================
# HELPERS
# =========================
def _sample_channels(n):
    channels = ["organic", "paid_ads", "referral", "partner"]
    probs = [
        DATA_CONFIG.organic_share,
        DATA_CONFIG.paid_ads_share,
        DATA_CONFIG.referral_share,
        DATA_CONFIG.partner_share,
    ]
    return np.random.choice(channels, size=n, p=probs)


def _sample_user_types(n):
    types = ["high_value", "medium_value", "low_value"]
    probs = [
        DATA_CONFIG.high_value_share,
        DATA_CONFIG.medium_value_share,
        DATA_CONFIG.low_value_share,
    ]
    return np.random.choice(types, size=n, p=probs)


def _assign_experiment(n):
    return np.random.choice(
        ["control", "treatment"],
        size=n,
        p=[1 - DATA_CONFIG.experiment_share, DATA_CONFIG.experiment_share],
    )


# =========================
# CHANNEL EFFECTS
# =========================
CHANNEL_EFFECTS = {
    "organic": {"signup": -0.05, "activation": 0.05, "conversion": 0.03},
    "paid_ads": {"signup": 0.08, "activation": -0.05, "conversion": -0.03},
    "referral": {"signup": 0.03, "activation": 0.08, "conversion": 0.02},
    "partner": {"signup": 0.02, "activation": 0.00, "conversion": 0.00},
}


# =========================
# USER TYPE EFFECTS
# =========================
USER_TYPE_EFFECTS = {
    "high_value": {"activation": 0.05, "conversion": 0.08, "revenue_mult": 1.5},
    "medium_value": {"activation": 0.00, "conversion": 0.00, "revenue_mult": 1.0},
    "low_value": {"activation": -0.05, "conversion": -0.07, "revenue_mult": 0.6},
}


# =========================
# MAIN GENERATION
# =========================
def generate_data():
    np.random.seed(DATA_CONFIG.random_seed)
    ensure_directories()

    n = DATA_CONFIG.n_users
    n_days = DATA_CONFIG.n_days

    # ---------------------
    # USERS
    # ---------------------
    users = pd.DataFrame({
        "user_id": np.arange(n),
        "signup_day": np.random.randint(0, n_days, size=n),
    })

    users["channel"] = _sample_channels(n)
    users["user_type"] = _sample_user_types(n)
    users["experiment_group"] = _assign_experiment(n)

    # ---------------------
    # EVENTS
    # ---------------------
    events = []

    for _, row in users.iterrows():
        uid = row["user_id"]
        signup_day = row["signup_day"]
        channel = row["channel"]
        user_type = row["user_type"]
        group = row["experiment_group"]

        # --- Base rates
        signup_p = DATA_CONFIG.signup_rate + CHANNEL_EFFECTS[channel]["signup"]
        activation_p = (
            DATA_CONFIG.activation_rate
            + CHANNEL_EFFECTS[channel]["activation"]
            + USER_TYPE_EFFECTS[user_type]["activation"]
        )
        conversion_p = (
            DATA_CONFIG.conversion_rate
            + CHANNEL_EFFECTS[channel]["conversion"]
            + USER_TYPE_EFFECTS[user_type]["conversion"]
        )

        # --- Treatment uplift
        if group == "treatment":
            signup_p += DATA_CONFIG.treatment_signup_uplift
            activation_p += DATA_CONFIG.treatment_activation_uplift
            conversion_p += DATA_CONFIG.treatment_conversion_uplift

        # Clip probabilities
        signup_p = np.clip(signup_p, 0.01, 0.99)
        activation_p = np.clip(activation_p, 0.01, 0.99)
        conversion_p = np.clip(conversion_p, 0.01, 0.99)

        # ---------------------
        # SIGNUP
        # ---------------------
        if np.random.rand() < signup_p:
            events.append([uid, signup_day, "signup", None])

            # ---------------------
            # ACTIVATION
            # ---------------------
            activation_day = signup_day + np.random.randint(1, 5)

            if activation_day < n_days and np.random.rand() < activation_p:
                events.append([uid, activation_day, "activation", None])

                # ---------------------
                # CONVERSION
                # ---------------------
                conversion_day = activation_day + np.random.randint(1, 10)

                if conversion_day < n_days and np.random.rand() < conversion_p:
                    revenue_base = DATA_CONFIG.avg_revenue_per_converter
                    revenue = (
                        revenue_base
                        * USER_TYPE_EFFECTS[user_type]["revenue_mult"]
                        + np.random.normal(0, DATA_CONFIG.revenue_noise_std)
                    )
                    revenue = max(5, revenue)

                    events.append([uid, conversion_day, "conversion", revenue])

                # ---------------------
                # CHURN
                # ---------------------
                churn_day = activation_day + np.random.randint(5, 30)
                if churn_day < n_days:
                    events.append([uid, churn_day, "churn", None])

    events_df = pd.DataFrame(events, columns=["user_id", "day", "event_type", "revenue"])

    # ---------------------
    # SAVE
    # ---------------------
    users.to_csv(DATA_DIR / "users.csv", index=False)
    events_df.to_csv(DATA_DIR / "events.csv", index=False)

    print("Data generated:")
    print(f"Users: {len(users)}")
    print(f"Events: {len(events_df)}")


if __name__ == "__main__":
    generate_data()