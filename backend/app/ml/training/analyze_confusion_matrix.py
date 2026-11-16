
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    classification_report
)

from app.ml.training.compare_classification_models import (
    prepare_classification_folds,
    prepare_features,
    create_model,
    select_best_threshold
)


def analyze_confusion_matrices():

    folds = prepare_classification_folds()

    for fold_number, (
        X_train,
        X_test,
        y_train,
        y_test,
        train_dates
    ) in enumerate(folds, start=1):

        X_train, X_test = prepare_features(
            X_train,
            X_test
        )

        threshold = select_best_threshold(
            X_train,
            y_train,
            train_dates
        )

        model = create_model()

        model.fit(
            X_train,
            y_train
        )

        probabilities = model.predict_proba(
            X_test
        )[:, 1]

        predictions = (
            probabilities >= threshold
        ).astype(int)

        cm = confusion_matrix(
            y_test,
            predictions,
            labels=[0, 1]
        )

        tn, fp, fn, tp = cm.ravel()

        print(f"\nFold {fold_number}")
        print("=" * 45)

        print(f"Selected threshold: {threshold:.2f}")

        print("\nConfusion Matrix:")
        print(cm)

        print("\nDetailed Results:")
        print(f"True Negative: {tn}")
        print(f"False Positive: {fp}")
        print(f"False Negative: {fn}")
        print(f"True Positive: {tp}")

        print("\nClassification Report:")

        print(
            classification_report(
                y_test,
                predictions,
                target_names=["DOWN", "UP"],
                zero_division=0
            )
        )


if __name__ == "__main__":
    analyze_confusion_matrices()
