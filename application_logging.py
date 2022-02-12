import os
import logging


def init_logger(logger_name: str = None):
    """Returns the instance to a logger. Creates a new instance if no instance exists."""

    if not logger_name:
        logger_name = "arc_logger"

    if logger_name in logging.root.manager.loggerDict:
        return logging.getLogger(logger_name)
    else:
        # Create a custom logger
        logger = logging.getLogger(logger_name)

        # check if loggin dir exists else create it
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
            os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

        # Create handlers
        logger.setLevel(logging.INFO)
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(f"logs/{logger_name}.log")

        # Create formatters and add it to handlers
        c_format = logging.Formatter("%(asctime)s [%(threadName)s] %(levelname)s - %(message)s")
        f_format = logging.Formatter("%(asctime)s [%(threadName)s] %(levelname)s - %(message)s")
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        return logger


def main():
    # start the kafka consumer.
    logger = init_logger()
    logger.info("TEST MEOW")


if __name__ == "__main__":
    main()
