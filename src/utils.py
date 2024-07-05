import logging


def setup_logging(logfile_path: str):
    """
    Setup logging configuration to log messages to both a file and the console.

    Args:
        logfile_path (str): Path to the log file where log messages will be saved.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(logfile_path), logging.StreamHandler()],
    )
