import sys

from loguru import logger


def setup_logging():
    """Initializes Loguru configuration once."""
    logger.remove()  # Clear default handler

    # Define your custom format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<cyan><level>{level: <5}</level></cyan> | "
        "<level>{message}</level>"
    )

    logger.add(sys.stderr, format=log_format, level="INFO")


# Run the setup immediately when this module is imported
setup_logging()
