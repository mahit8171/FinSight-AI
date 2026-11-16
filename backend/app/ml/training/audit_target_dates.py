
import numpy as np
import pandas as pd

from app.ml.data.load_data import load_stock_data
from app.ml.data.clean_data import clean_stock_data
from app.ml.features.build_features import build_features

from app.db.database import SessionLocal
from app.models.stock import Stock


def audit_target_dates():

    db = SessionLocal()

    try:
        stocks = db.query(Stock.symbol).order_by(
            Stock.symbol
        ).all()

        print("\nTARGET ALIGNMENT AUDIT")
        print("=" * 65)

        for (symbol,) in stocks:

            # Original cleaned data
            raw_df = load_stock_data(db, symbol)
            raw_df = clean_stock_data(raw_df)

            raw_df = raw_df.sort_values(
                "date"
            ).reset_index(drop=True)

            # Expected next observation from raw data
            raw_df["expected_target_date"] = (
                raw_df["date"].shift(-1)
            )

            raw_df["expected_target"] = (
                raw_df["close"].shift(-1)
            )

            expected = raw_df[
                ["date", "expected_target_date", "expected_target"]
            ]

            # Actual feature-engineered dataset
            feature_df = build_features(raw_df.drop(
                columns=[
                    "expected_target_date",
                    "expected_target"
                ]
            ))

            merged = feature_df.merge(
                expected,
                on="date",
                how="left"
            )

            date_match = (
                merged["target_date"].reset_index(drop=True)
                ==
                merged["expected_target_date"].reset_index(drop=True)
            ).all()

            price_match = np.isclose(
                merged["target"].to_numpy(dtype=float),
                merged["expected_target"].to_numpy(dtype=float),
                equal_nan=True
            ).all()

            print(f"\nStock: {symbol}")
            print(f"Rows: {len(merged)}")
            print(f"Target date match: {date_match}")
            print(f"Target price match: {price_match}")

            if not date_match or not price_match:

                mismatch = merged[
                    (
                        merged["target_date"]
                        != merged["expected_target_date"]
                    )
                    |
                    (
                        ~np.isclose(
                            merged["target"],
                            merged["expected_target"],
                            equal_nan=True
                        )
                    )
                ]

                print("\nMismatched records:")

                print(
                    mismatch[
                        [
                            "date",
                            "target_date",
                            "expected_target_date",
                            "target",
                            "expected_target"
                        ]
                    ].head(10).to_string(index=False)
                )

    finally:
        db.close()


if __name__ == "__main__":
    audit_target_dates()
