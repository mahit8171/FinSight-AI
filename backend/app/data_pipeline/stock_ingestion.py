
import yfinance as yf
import pandas as pd

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.stock_price_service import stock_price_service
from app.data_pipeline.config import STOCKS, DEFAULT_PERIOD
from app.repositories.stock_repository import stock_repository
from app.repositories.stock_price_repository import stock_price_repository



def get_yahoo_symbol(symbol: str) -> str:
    if symbol.endswith(".NS") or symbol.endswith(".BO"):
        return symbol

    return f"{symbol}.NS"



def fetch_stock_data(
    symbol: str,
    period: str = "1y",
    start=None
) -> pd.DataFrame:

    yahoo_symbol = get_yahoo_symbol(symbol)
    ticker = yf.Ticker(yahoo_symbol)

    if start is not None:
        data = ticker.history(
            start=start,
            period=None,
            auto_adjust=True
        )
    else:
        data = ticker.history(
            period=period,
            auto_adjust=True
        )

    if data.empty:
        return pd.DataFrame()

    return data




def clean_stock_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop(
        columns=["Dividends", "Stock Splits"],
        errors="ignore"
    )

    data = data.reset_index()
    data = data.drop_duplicates(subset=["Date"])
    data = data.dropna()
    data = data.sort_values("Date")
    data = data.reset_index(drop=True)

    return data



def run_stock_ingestion(symbol: str, period: str = "1y"):
    db: Session = SessionLocal()

    try:
        print(f"Starting incremental ingestion: {symbol}")

        # 1. Find stock in database
        stock = stock_repository.get_by_symbol(db, symbol)

        if stock is None:
            raise ValueError(f"Stock {symbol} not found")

        # 2. Find latest stored date
        next_fetch_date = stock_price_service.get_next_fetch_date(
            db=db,
            stock_id=stock.id
        )

        # 3. Fetch data
        if next_fetch_date is None:
            print("No historical data found. Fetching initial data.")

            raw_data = fetch_stock_data(
                symbol=symbol,
                period=period
            )
        else:
            print(f"Fetching data from: {next_fetch_date}")

            raw_data = fetch_stock_data(
                symbol=symbol,
                start=next_fetch_date
            )

        # 4. Handle empty data
        if raw_data.empty:
            print(f"No new data available for {symbol}")

            return {
                "message": "No new data available",
                "symbol": symbol,
                "total_records": 0
            }

        # 5. Clean data
        clean_data = clean_stock_data(raw_data)

        # 6. Save new records
        result = stock_price_service.save_stock_prices(
            db=db,
            symbol=symbol,
            data=clean_data
        )

        print("Incremental ingestion completed!")
        print(result)

        return result

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()




def run_multiple_stock_ingestion():
    results = []

    for stock in STOCKS:
        symbol = stock["symbol"]

        print(f"\n{'=' * 40}")
        print(f"Starting ingestion: {symbol}")
        print(f"{'=' * 40}")

        try:
            result = run_stock_ingestion(
                symbol=symbol,
                period=DEFAULT_PERIOD
            )

            results.append({
                "symbol": symbol,
                "status": "success",
                "records": result["total_records"]
            })

        except Exception as e:
            print(f"Failed for {symbol}: {e}")

            results.append({
                "symbol": symbol,
                "status": "failed",
                "error": str(e)
            })

    print("\n========== INGESTION SUMMARY ==========")

    for result in results:
        print(result)

    return results


if __name__ == "__main__":
    run_multiple_stock_ingestion()

