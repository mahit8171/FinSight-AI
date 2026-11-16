
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from app.ml.data.prepare_multi_stock_dataset import (
    prepare_multi_stock_dataset
)


TOP_FEATURES = [
    "high_ratio",
    "open_ratio",
    "volume_change",
    "low_ratio",
    "volatility_5",
]


def prepare_classification_folds():

    df = prepare_multi_stock_dataset()

    df["target_direction"] = (
        df["target_return"] > 0
    ).astype(int)

    dates = sorted(df["date"].unique())

    initial_train_size = int(len(dates) * 0.40)
    remaining_dates = dates[initial_train_size:]

    test_date_groups = [
        list(group)
        for group in np.array_split(remaining_dates, 3)
    ]

    folds = []
    train_dates = list(dates[:initial_train_size])

    for test_dates in test_date_groups:

        if not test_dates:
            continue

        test_start_date = min(test_dates)

        train_df = df[
            df["date"].isin(train_dates)
        ].copy()

        test_df = df[
            df["date"].isin(test_dates)
        ].copy()

        # Outer validation leakage protection
        train_df = train_df[
            train_df["target_date"] < test_start_date
        ].copy()

        X_train = train_df[
            TOP_FEATURES + ["symbol"]
        ].reset_index(drop=True)

        X_test = test_df[
            TOP_FEATURES + ["symbol"]
        ].reset_index(drop=True)

        y_train = train_df[
            "target_direction"
        ].reset_index(drop=True)

        y_test = test_df[
            "target_direction"
        ].reset_index(drop=True)

        train_date_series = train_df[
            "date"
        ].reset_index(drop=True)

        train_target_date_series = train_df[
            "target_date"
        ].reset_index(drop=True)

        leakage_check = (
            train_df["target_date"].max()
            < test_df["date"].min()
        )

        print(f"\nClassification Fold {len(folds) + 1}")
        print(f"Training rows: {len(X_train)}")
        print(f"Testing rows: {len(X_test)}")
        print("Outer leakage check:", leakage_check)

        if not leakage_check:
            raise ValueError("Outer validation leakage detected")

        folds.append((
            X_train,
            X_test,
            y_train,
            y_test,
            train_date_series,
            train_target_date_series
        ))

        train_dates.extend(test_dates)

    return folds


def prepare_features(X_train, X_test):

    X_train = pd.get_dummies(
        X_train.copy(),
        columns=["symbol"],
        dtype=int
    )

    X_test = pd.get_dummies(
        X_test.copy(),
        columns=["symbol"],
        dtype=int
    )

    X_test = X_test.reindex(
        columns=X_train.columns,
        fill_value=0
    )

    return X_train, X_test


def create_model():

    return RandomForestClassifier(
        n_estimators=200,
        max_depth=5,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )


def select_best_threshold(
    X_train,
    y_train,
    train_dates,
    train_target_dates
):

    unique_dates = sorted(train_dates.unique())

    split_index = int(len(unique_dates) * 0.80)

    model_train_dates = unique_dates[:split_index]
    validation_dates = unique_dates[split_index:]

    if not model_train_dates or not validation_dates:
        raise ValueError(
            "Insufficient dates for threshold validation"
        )

    validation_start_date = min(validation_dates)

    # Internal training must not have targets
    # falling on or after validation start.
    model_train_mask = (
        train_dates.isin(model_train_dates)
        & (train_target_dates < validation_start_date)
    )

    validation_mask = train_dates.isin(
        validation_dates
    )

    X_model_train = X_train.loc[
        model_train_mask
    ]

    y_model_train = y_train.loc[
        model_train_mask
    ]

    X_validation = X_train.loc[
        validation_mask
    ]

    y_validation = y_train.loc[
        validation_mask
    ]

    if X_model_train.empty or X_validation.empty:
        raise ValueError(
            "Internal training or validation dataset is empty"
        )

    # Verify internal leakage boundary
    latest_train_target = train_target_dates.loc[
        model_train_mask
    ].max()

    earliest_validation_date = train_dates.loc[
        validation_mask
    ].min()

    leakage_check = (
        latest_train_target < earliest_validation_date
    )

    print("\nInternal Validation Leakage Check:")
    print("Latest training target:", latest_train_target)
    print("Earliest validation date:", earliest_validation_date)
    print("Leakage check:", leakage_check)

    if not leakage_check:
        raise ValueError(
            "Internal validation leakage detected"
        )

    model = create_model()

    model.fit(
        X_model_train,
        y_model_train
    )

    validation_probabilities = model.predict_proba(
        X_validation
    )[:, 1]

    thresholds = np.arange(
        0.30,
        0.71,
        0.05
    )

    threshold_results = []

    for threshold in thresholds:

        predictions = (
            validation_probabilities >= threshold
        ).astype(int)

        f1 = f1_score(
            y_validation,
            predictions,
            zero_division=0
        )

        threshold_results.append({
            "threshold": threshold,
            "f1": f1
        })

    best_result = max(
        threshold_results,
        key=lambda result: (
            result["f1"],
            -abs(result["threshold"] - 0.50)
        )
    )

    print("\nValidation Threshold Results")

    for result in threshold_results:
        print(
            f"Threshold: {result['threshold']:.2f} | "
            f"F1: {result['f1']:.4f}"
        )

    return best_result["threshold"]


def evaluate_classification():

    folds = prepare_classification_folds()

    results = []

    for fold_number, (
        X_train,
        X_test,
        y_train,
        y_test,
        train_dates,
        train_target_dates
    ) in enumerate(folds, start=1):

        X_train, X_test = prepare_features(
            X_train,
            X_test
        )

        best_threshold = select_best_threshold(
            X_train,
            y_train,
            train_dates,
            train_target_dates
        )

        print(
            f"\nFold {fold_number} selected threshold: "
            f"{best_threshold:.2f}"
        )

        # Refit on complete outer training data
        final_model = create_model()

        final_model.fit(
            X_train,
            y_train
        )

        probabilities = final_model.predict_proba(
            X_test
        )[:, 1]

        predictions = (
            probabilities >= best_threshold
        ).astype(int)

        results.append({
            "Fold": fold_number,
            "Model": "Tuned Random Forest",
            "Threshold": best_threshold,
            "Accuracy": accuracy_score(y_test, predictions),
            "Precision": precision_score(
                y_test, predictions, zero_division=0
            ),
            "Recall": recall_score(
                y_test, predictions, zero_division=0
            ),
            "F1": f1_score(
                y_test, predictions, zero_division=0
            ),
            "ROC-AUC": roc_auc_score(
                y_test, probabilities
            )
        })

        # Majority-class baseline
        majority_class = int(
            y_train.value_counts().idxmax()
        )

        baseline_predictions = np.full(
            len(y_test),
            majority_class
        )

        results.append({
            "Fold": fold_number,
            "Model": "Majority Baseline",
            "Threshold": None,
            "Accuracy": accuracy_score(
                y_test, baseline_predictions
            ),
            "Precision": precision_score(
                y_test,
                baseline_predictions,
                zero_division=0
            ),
            "Recall": recall_score(
                y_test,
                baseline_predictions,
                zero_division=0
            ),
            "F1": f1_score(
                y_test,
                baseline_predictions,
                zero_division=0
            ),
            "ROC-AUC": np.nan
        })

    results_df = pd.DataFrame(results)

    print("\nClassification Results")
    print("=" * 90)
    print(results_df.to_string(index=False))

    print("\nAverage Model Performance")
    print("=" * 90)

    summary = (
        results_df.groupby("Model")[
            ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]
        ]
        .mean()
    )

    print(summary.to_string())


if __name__ == "__main__":
    evaluate_classification()
