
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    balanced_accuracy_score
)

from app.ml.training.compare_classification_models import (
    prepare_classification_folds,
    prepare_features,
    create_model,
    select_best_threshold
)


def calculate_metrics(y_true, predictions):

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1]
    ).ravel()

    specificity = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else 0
    )

    return {
        "Accuracy": accuracy_score(
            y_true, predictions
        ),

        "Precision": precision_score(
            y_true,
            predictions,
            zero_division=0
        ),

        "Recall": recall_score(
            y_true,
            predictions,
            zero_division=0
        ),

        "Specificity": specificity,

        "F1": f1_score(
            y_true,
            predictions,
            zero_division=0
        ),

        "Balanced Accuracy": balanced_accuracy_score(
            y_true,
            predictions
        )
    }


def compare_threshold_strategies():

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

        print(f"\n{'=' * 60}")
        print(f"FOLD {fold_number}")
        print("=" * 60)

        # Prepare categorical features
        X_train, X_test = prepare_features(
            X_train,
            X_test
        )

        # Select threshold using internal validation
        # with target-date leakage protection
        best_threshold = select_best_threshold(
            X_train,
            y_train,
            train_dates,
            train_target_dates
        )

        print(
            f"\nFold {fold_number} - "
            f"Best Threshold: {best_threshold:.2f}"
        )

        # Train final model on complete outer training data
        model = create_model()

        model.fit(
            X_train,
            y_train
        )

        # Predict probabilities on untouched test data
        probabilities = model.predict_proba(
            X_test
        )[:, 1]

        # Compare default and tuned thresholds
        thresholds = list(dict.fromkeys([
            0.50,
            best_threshold
        ]))

        for threshold in thresholds:

            predictions = (
                probabilities >= threshold
            ).astype(int)

            metrics = calculate_metrics(
                y_test,
                predictions
            )

            results.append({
                "Fold": fold_number,
                "Threshold": threshold,
                **metrics
            })

            print(
                f"\nThreshold: {threshold:.2f}"
            )

            for metric_name, metric_value in metrics.items():
                print(
                    f"{metric_name}: {metric_value:.4f}"
                )

    # Convert results into DataFrame
    results_df = pd.DataFrame(results)

    print("\nThreshold Strategy Comparison")
    print("=" * 100)

    print(
        results_df.round(4).to_string(index=False)
    )

    # Average performance
    print("\nAverage Metrics")
    print("=" * 100)

    summary = (
        results_df.groupby("Threshold")[
            [
                "Accuracy",
                "Precision",
                "Recall",
                "Specificity",
                "F1",
                "Balanced Accuracy"
            ]
        ]
        .mean()
    )

    print(
        summary.round(4).to_string()
    )


if __name__ == "__main__":
    compare_threshold_strategies()
