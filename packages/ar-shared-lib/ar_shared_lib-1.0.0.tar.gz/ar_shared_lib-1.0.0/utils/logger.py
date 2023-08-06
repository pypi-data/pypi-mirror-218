import logging
import os
from typing import Optional

DEFAULT_LOG_FORMAT = "[%(levelname)s] - %(name)s | %(asctime)s || %(message)s"


def setup_logger(log_level: int = logging.INFO,
                 log_format: Optional[str] = DEFAULT_LOG_FORMAT):
    """Local logger setup"""
    logging.basicConfig(
        level=log_level,
        format=log_format,
    )


def get_aws_lambda_logger(logger_name: Optional[str] = None,
                          log_level: Optional[str] = logging.INFO,
                          log_format: Optional[str] = DEFAULT_LOG_FORMAT,
                          environment: Optional[str] = "dev"):
    """AWS lambda logger setup.
    
    Configurations for AWS logger
    https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
    """
    environment = environment or os.getenv("ENVIRONMENT")

    # local logger configurations
    if environment == "dev":
        logging.basicConfig(level=log_level, format=log_format)
        logger = logging.getLogger(logger_name)

    # AWS has its own handler for root logger
    # the next lines are configure the log level for predefined AWS logger
    else:
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

    return logger
