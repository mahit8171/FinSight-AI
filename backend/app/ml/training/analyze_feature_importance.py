
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from app.ml.data.prepare_multi_stock_dataset import (
    prepare_multi_stock_dataset
)
from app.ml.data.prepare_dataset import FEATURE_COLUMNS


def analyze_feature_importance():

    df = prepare_multi_stock_dataset()

    # Chronological split: first 80% dates for training
    dates = sorted(df["date"].unique())
    split_index = int(len(dates) * 0.80)

    train_dates = dates[:split_index]

    train_df = df[
        df["date"].isin(train_dates)
    ].copy()

    # Prevent target leakage across the split
    test_start_date = dates[split_index]

    train_df = train_df[
        train_df["target_date"] < test_start_date
    ].copy()

    X_train = train_df[
        FEATURE_COLUMNS + ["symbol"]
    ]

    y_train = train_df["target_return"]

    # Convert stock symbols into numeric columns
    X_train = pd.get_dummies(
        X_train,
        columns=["symbol"],
        dtype=int
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=5,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    importance = pd.Series(
        model.feature_importances_,
        index=X_train.columns
    ).sort_values(ascending=False)

    print("\nRandom Forest Feature Importance")
    print("-" * 45)

    print(importance.to_string())

    print("\nTop 5 Features")
    print("-" * 45)

    print(importance.head(5).to_string())


if __name__ == "__main__":
    analyze_feature_importance()
