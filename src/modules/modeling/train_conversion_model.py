import json
import os

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.common.paths import ARTIFACTS_DIR
from src.common.schema import (
    CHANNEL_COL,
    CONVERSION_EVENT,
    CONVERTED_COL,
    EVENT_TYPE_COL,
    EXPERIMENT_GROUP_COL,
    MODEL_TARGET_COL,
    SIGNUP_DAY_COL,
    USER_ID_COL,
    USER_TYPE_COL,
)


DATA_DIR = os.path.join(ARTIFACTS_DIR, "data")
MODELING_DIR = os.path.join(ARTIFACTS_DIR, "modeling")

USERS_PATH = os.path.join(DATA_DIR, "users.csv")
EVENTS_PATH = os.path.join(DATA_DIR, "events.csv")

MODEL_METRICS_PATH = os.path.join(MODELING_DIR, "conversion_model_metrics.json")
MODEL_DATASET_PATH = os.path.join(MODELING_DIR, "conversion_model_dataset.csv")
MODEL_PREDICTIONS_PATH = os.path.join(MODELING_DIR, "conversion_model_predictions.csv")


def build_user_level_dataset(users: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    conversion_flags = (
        events.loc[events[EVENT_TYPE_COL] == CONVERSION_EVENT, [USER_ID_COL]]
        .drop_duplicates()
    )
    conversion_flags[CONVERTED_COL] = 1

    modeling_df = users.copy()
    modeling_df = modeling_df.merge(conversion_flags, on=USER_ID_COL, how="left")
    modeling_df[CONVERTED_COL] = modeling_df[CONVERTED_COL].fillna(0).astype(int)

    return modeling_df


def build_model_pipeline() -> Pipeline:
    categorical_features = [
        CHANNEL_COL,
        USER_TYPE_COL,
        EXPERIMENT_GROUP_COL,
    ]
    numeric_features = [SIGNUP_DAY_COL]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
            ("numeric", "passthrough", numeric_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )

    return model


def fit_conversion_model(modeling_df: pd.DataFrame) -> tuple[dict, Pipeline]:
    feature_cols = [
        SIGNUP_DAY_COL,
        CHANNEL_COL,
        USER_TYPE_COL,
        EXPERIMENT_GROUP_COL,
    ]

    X = modeling_df[feature_cols].copy()
    y = modeling_df[MODEL_TARGET_COL].copy()

    model = build_model_pipeline()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "n_users": int(len(modeling_df)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "positive_rate": float(y.mean()),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "features_used": feature_cols,
        "target": MODEL_TARGET_COL,
    }

    return metrics, model


def build_predictions_table(modeling_df: pd.DataFrame, model: Pipeline) -> pd.DataFrame:
    feature_cols = [
        SIGNUP_DAY_COL,
        CHANNEL_COL,
        USER_TYPE_COL,
        EXPERIMENT_GROUP_COL,
    ]

    X_all = modeling_df[feature_cols].copy()
    predicted_probabilities = model.predict_proba(X_all)[:, 1]

    predictions_df = modeling_df[
        [
            USER_ID_COL,
            MODEL_TARGET_COL,
            CHANNEL_COL,
            USER_TYPE_COL,
            EXPERIMENT_GROUP_COL,
        ]
    ].copy()

    predictions_df["predicted_probability"] = predicted_probabilities

    return predictions_df


def train_conversion_model() -> dict:
    os.makedirs(MODELING_DIR, exist_ok=True)

    users = pd.read_csv(USERS_PATH)
    events = pd.read_csv(EVENTS_PATH)

    modeling_df = build_user_level_dataset(users=users, events=events)
    metrics, model = fit_conversion_model(modeling_df=modeling_df)
    predictions_df = build_predictions_table(modeling_df=modeling_df, model=model)

    modeling_df.to_csv(MODEL_DATASET_PATH, index=False)
    predictions_df.to_csv(MODEL_PREDICTIONS_PATH, index=False)

    with open(MODEL_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Conversion model training completed.")
    print(f"User-level dataset saved to: {MODEL_DATASET_PATH}")
    print(f"Model metrics saved to: {MODEL_METRICS_PATH}")
    print(f"Model predictions saved to: {MODEL_PREDICTIONS_PATH}")
    print("\nModel Performance")
    print(f"Users: {metrics['n_users']}")
    print(f"Positive Rate: {metrics['positive_rate']:.4f}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"ROC-AUC: {metrics['roc_auc']:.4f}")

    return metrics


if __name__ == "__main__":
    train_conversion_model()