import logging
import logging.config
import sys


def logging_setup(path="/tmp/BrowserAutomator.log", level=logging.INFO):
    logger = logging.getLogger("BrowserAutomator")
    if level:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        if path:
            file_handler = logging.FileHandler(path)
            file_handler.setLevel(level)
            file_formatter = logging.Formatter("%(asctime)s %(levelname)s - %(name)s - %(module)s - %(funcName)s: %(message)s")
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        sys.excepthook = handle_exception
    else:
        logger.propagate = False


def handle_exception(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger(__name__)
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


if __name__ == "__main__":
    logging_setup()
