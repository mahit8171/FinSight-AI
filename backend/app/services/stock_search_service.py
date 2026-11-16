
from sqlalchemy.orm import Session

from app.repositories.stock_repository import stock_repository


class StockSearchService:

    def search_stocks(
        self,
        db: Session,
        query: str,
        limit: int = 10
    ):
        return stock_repository.search(
            db=db,
            query=query,
            limit=limit
        )


stock_search_service = StockSearchService()
