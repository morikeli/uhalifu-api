from pathlib import Path

import polars as pl

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = Path(BASE_DIR, "data/global-terrorism.csv")


def load_data():
    """
    Load and preprocess terrorism dataset from CSV file.
    Reads a CSV file containing terrorism incident data and performs the following operations:
    - Selects relevant columns for analysis including date, location, attack, and target information
    - Removes rows with null values in critical fields (provstate, country_txt, latitude, longitude)
    
    Returns:
        pl.DataFrame: A polars DataFrame containing preprocessed terrorism incident data with columns:
            - iyear, imonth, iday: Date information
            - country_txt, region_txt, provstate, city, location: Location details
            - latitude, longitude: Geographic coordinates
            - attacktype1_txt: Type of attack
            - targtype1_txt: Type of target
            - summary: Incident summary
            - suicide: Whether attack was suicide-related
    """

    df = pl.read_csv(
        DATA_PATH,
        encoding="utf8-lossy",
        ignore_errors=True,
    )

    return df.select(
        [
            "iyear",
            "imonth",
            "iday",
            "country_txt",
            "region_txt",
            "provstate",
            "city",
            "location",
            "latitude",
            "longitude",
            "attacktype1_txt",
            "targtype1_txt",
            "summary",
            "suicide",
        ]
    ).drop_nulls(["provstate", "country_txt", "latitude", "longitude"])
