import logging


def get_logger(name="app"):
    logger = logging.getLogger("my_app")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers when Streamlit reruns
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    logger.info("Logger initialized — this prints to the console")

    return logger
