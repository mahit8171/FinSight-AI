
from app.ml.data.prepare_multi_stock_split import (
    prepare_multi_stock_split
)
from app.ml.data.prepare_dataset import FEATURE_COLUMNS

from sklearn.linear_model import LinearRegression


def inspect_features():

    X_train, X_test, y_train, y_test = prepare_multi_stock_split()

    model = LinearRegression()
    model.fit(X_train[FEATURE_COLUMNS], y_train)

    for name, coefficient in sorted(
        zip(FEATURE_COLUMNS, model.coef_),
        key=lambda item: abs(item[1]),
        reverse=True
    ):
        print(f"{name}: {coefficient:.8f}")

    print("\nIntercept:", model.intercept_)


if __name__ == "__main__":
    inspect_features()
