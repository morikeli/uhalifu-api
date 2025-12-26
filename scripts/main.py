import asyncio
import time
from datetime import datetime, timezone

import uvloop
from app.core.database import init_db, AsyncSessionLocal, close_db
from app.models import Location
from .logger import setup_logging
from loguru import logger

from .data import load_data


async def main():
    """
    Main coroutine that loads terrorism data from CSV and inserts it into the database.

    Loads data from a CSV file, initializes the database connection, creates Location
    objects for each row, and bulk inserts them into the database. Logs timing information
    for performance monitoring.
    """

    start_total = time.perf_counter()

    # Load csv file
    t0 = time.perf_counter()
    df = load_data()
    t1 = time.perf_counter()

    logger.info(f"CSV loaded in {(t1 - t0):.2f} seconds")
    logger.info(f"Total rows to process: {len(df):,}")

    # Initialize database connection
    await init_db()

    # Iterate rows in the dataframe and insert into db
    start_rw_time = time.perf_counter()  # Start read/write timer

    async with AsyncSessionLocal() as session:
        locations = []  # Collect Location objects for bulk insert

        # Process each row from the dataframe
        for row_num, row in enumerate(df.iter_rows(named=True), start=1):
            location = Location(
                year=row["iyear"],
                month=row["imonth"],
                day=row["iday"],
                country=row["country_txt"],
                region=row["region_txt"],
                province=row["provstate"],
                city=row["city"],
                location=row["location"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                attack_type=row["attacktype1_txt"],
                target=row["targtype1_txt"],
                description=row["summary"],
                suicide_bombing=bool(row["suicide"]),
                date_created=datetime.now(timezone.utc),
            )

            locations.append(location)

            # Log progress every 10k rows
            if row_num % 10_000 == 0:
                logger.info(f"{row_num:,} rows processed...")

        # Bulk insert all locations and commit transaction
        session.add_all(locations)
        await session.commit()
        await close_db()

    final_rw_time = time.perf_counter()  # End read/write timer

    # Log performance metrics
    total_time = time.perf_counter() - start_total

    logger.success(f"DB insert time: {final_rw_time - start_rw_time:.2f}s")
    logger.success(f"Total runtime: {total_time:.2f}s")


if __name__ == "__main__":
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        runner.run(main())
