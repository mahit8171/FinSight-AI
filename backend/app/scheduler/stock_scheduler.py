
from pathlib import Path
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from app.data_pipeline.stock_ingestion import (
    run_multiple_stock_ingestion
)


# ==========================================
# 1. Create logs directory
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[3]

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "stock_ingestion.log"


# ==========================================
# 2. Configure logging
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


# ==========================================
# 3. Create scheduler
# ==========================================

scheduler = BlockingScheduler(
    timezone="Asia/Kolkata"
)


# ==========================================
# 4. Daily stock ingestion job
# ==========================================

def daily_stock_ingestion():

    logger.info("Daily stock ingestion started")

    try:

        results = run_multiple_stock_ingestion()

        logger.info("Daily stock ingestion completed")
        logger.info("Results: %s", results)

    except Exception:

        logger.exception("Daily stock ingestion failed")


# ==========================================
# 5. Schedule job at 6:00 PM IST
# ==========================================

scheduler.add_job(
    daily_stock_ingestion,
    trigger=CronTrigger(
        hour=18,
        minute=0,
        timezone="Asia/Kolkata"
    ),
    id="daily_stock_ingestion",
    name="Daily Stock Data Ingestion",
    replace_existing=True,
    max_instances=1
)


# ==========================================
# 6. Start scheduler
# ==========================================

if __name__ == "__main__":

    logger.info("Starting FinSight AI Stock Scheduler")

    try:

        scheduler.start()

    except (KeyboardInterrupt, SystemExit):

        logger.info("Scheduler stopped")
