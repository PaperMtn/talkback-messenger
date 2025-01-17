"""Utility functions for the Talkback Messenger

This module contains utility functions that are used throughout the Talkback Messenger

Typical usage example:
    from talkback_messenger.utils import load_config
    config = load_config('config.yaml')
"""

import sys
from typing import Dict, Any, Tuple

import yaml
from loguru import logger

from talkback_messenger.models.resource import Resource
from talkback_messenger.models.subscription import Subscription


def load_config(filepath: str) -> Dict[str, Any] | None:
    """Load configuration from YAML config file

    Args:
        filepath: Path to the YAML configuration file
    Returns:
        Dictionary containing the configuration
    """

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return None


def deduplicate_results(resource_list: list[Tuple[Resource, Subscription]]) \
        -> list[Tuple[Resource, Subscription]]:
    """Deduplicate a list of resources based on their id

    Args:
        resource_list: List of tuples containing Resource and Subscription objects
    Returns:
        List of deduplicated tuples containing Resource and Subscription objects
    """

    deduplicated_resources = []
    seen_ids = set()
    for res, sub in resource_list:
        if res.id not in seen_ids:
            deduplicated_resources.append((res, sub))
            seen_ids.add(res.id)
    return deduplicated_resources


async def init_logger(debug: bool) -> None:
    """Initialise the Loguru logger

    Args:
        debug: Whether debug logging should be enabled
    """

    logger.remove()
    log_format = ('<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{'
                  'message}</level>')
    if debug:
        logger.add(sys.stdout, level='DEBUG', format=log_format)
        logger.debug('Logging level set to DEBUG')
    else:
        logger.add(sys.stdout, level='INFO', format=log_format)
        logger.info('Logging level set to INFO')
