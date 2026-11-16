
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from app.ml.data.prepare_multi_stock_split import (
    prepare_multi_stock_split
)
from app.ml.data.prepare_dataset import FEATURE_COLUMNS


def train_encoded_model():

    X_train, X_test, y_train, y_test = prepare_multi_stock_split()

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "stock",
                OneHotEncoder(handle_unknown="ignore"),
                ["symbol"]
            ),
            (
                "numeric",
                "passthrough",
                FEATURE_COLUMNS
            )
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", LinearRegression())
        ]
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print("\nEncoded Linear Regression Evaluation")
    print("Training samples:", len(X_train))
    print("Testing samples:", len(X_test))
    print(f"MAE: {mae:.6f}")
    print(f"RMSE: {rmse:.6f}")
    print(f"R2 Score: {r2:.4f}")

    return model


if __name__ == "__main__":
    train_encoded_model()
