import pandas as pd

from src.common.paths import ARTIFACTS_DIR


USERS_PATH = ARTIFACTS_DIR / "data" / "users.csv"
EVENTS_PATH = ARTIFACTS_DIR / "data" / "events.csv"

OUTPUT_DIR = ARTIFACTS_DIR / "funnel"
OUTPUT_PATH = OUTPUT_DIR / "experiment_funnel.csv"


def compute_experiment_funnel():
    print("\n===== EXPERIMENT FUNNEL ANALYSIS =====")

    # =========================
    # LOAD DATA
    # =========================
    print("Loading users and events...")
    users = pd.read_csv(USERS_PATH)
    events = pd.read_csv(EVENTS_PATH)

    # =========================
    # JOIN
    # =========================
    print("Joining users with events...")
    df = events.merge(users, on="user_id", how="left")

    # =========================
    # USER-LEVEL FLAGS
    # =========================
    print("Building user-level funnel flags...")

    signup = df[df["event_type"] == "signup"].groupby("user_id").size().rename("signup")
    activation = df[df["event_type"] == "activation"].groupby("user_id").size().rename("activation")
    conversion = df[df["event_type"] == "conversion"].groupby("user_id").size().rename("conversion")

    user_df = users.copy()
    user_df = user_df.merge(signup, on="user_id", how="left")
    user_df = user_df.merge(activation, on="user_id", how="left")
    user_df = user_df.merge(conversion, on="user_id", how="left")

    # Convert to binary flags
    for col in ["signup", "activation", "conversion"]:
        user_df[col] = user_df[col].fillna(0)
        user_df[col] = (user_df[col] > 0).astype(int)

    # =========================
    # AGGREGATE BY GROUP
    # =========================
    print("Aggregating funnel metrics...")

    summary = user_df.groupby("experiment_group").agg(
        users=("user_id", "count"),
        signup_users=("signup", "sum"),
        activation_users=("activation", "sum"),
        conversion_users=("conversion", "sum"),
    )

    # =========================
    # FUNNEL METRICS
    # =========================
    print("Computing funnel rates...")

    summary["signup_rate"] = summary["signup_users"] / summary["users"]
    summary["activation_rate"] = summary["activation_users"] / summary["signup_users"]
    summary["conversion_given_activation"] = summary["conversion_users"] / summary["activation_users"]
    summary["overall_conversion_rate"] = summary["conversion_users"] / summary["users"]

    print("\n===== FUNNEL SUMMARY =====")
    print(summary)

    # =========================
    # SAVE
    # =========================
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_PATH)

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    compute_experiment_funnel()