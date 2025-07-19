"""
Module for configuring logging in the application.
"""
import logging


def setup_logging():
    """
    Configures the logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()],
        force=True
    )
