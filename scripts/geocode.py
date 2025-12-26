import asyncio
import os

import httpx
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


@logger.catch
async def geocode_location(place: str):
    params = {"q": place, "key": API_KEY, "format": "json"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(BASE_URL, params=params)
            r.raise_for_status()
            data = r.json()[0]

            await asyncio.sleep(3)  # To respect rate limits

            logger.info(
                f"Geocoding successful for {place}: {
                    data['lat']}, {data['lon']}"
            )
            return float(data["lat"]), float(data["lon"])

    except Exception as e:
        logger.warning(f"Geocoding failed for {place}: {e}")
        return None, None
