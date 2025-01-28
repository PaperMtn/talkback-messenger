"""Module for Subscription model

Typical usage example:
    from talkback_messenger.models import subscription
    sub = subscription.create_subscription_from_dict(subscription_dict)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Union, Optional

from talkback_messenger.exceptions import InvalidSubscriptionError, MissingSubscriptionsError
from talkback_messenger.models.utils import validate_fields

DEFAULT_RANK = 80.00
DEFAULT_RESOURCE_TYPES = ['post', 'news', 'oss', 'video', 'paper', 'slides', 'n_a']
DEFAULT_CURATED = False


@dataclass(slots=True)
class SlackConfig:
    """Slack users and channels to send messages to"""
    users: Optional[List[str]] = field(default_factory=list)
    channels: Optional[List[str]] = field(default_factory=list)

    def __post_init__(self):
        validate_fields(self, {'users': list, 'channels': list})


@dataclass(slots=True)
class Filters:
    """Filters to use with the subscription to narrow down resources"""
    rank: Optional[Union[int, float]] = DEFAULT_RANK
    resource_types: Optional[List[str]] = field(default_factory=lambda: DEFAULT_RESOURCE_TYPES)
    curated: Optional[bool] = DEFAULT_CURATED

    def __post_init__(self):
        validate_fields(self, {
            'rank': (int, float),
            'resource_types': list,
            'curated': bool
        })


@dataclass(slots=True)
class Subscription:
    """Subscription for Talkback resources"""
    subscription_type: str
    id: str
    query: str
    filters: Filters
    slack_destinations: Optional[SlackConfig] = None

    def __post_init__(self):
        validate_fields(self, {
            'subscription_type': str,
            'id': str,
            'query': str
        })


def _create_filters(filters_dict: Dict) -> Filters:
    """Create Filters object from a dictionary."""
    rank = filters_dict.get('rank', DEFAULT_RANK)
    try:
        rank = float(rank)
    except (ValueError, TypeError):
        rank = DEFAULT_RANK

    return Filters(
        rank=rank,
        resource_types=filters_dict.get('resource_types', DEFAULT_RESOURCE_TYPES),
        curated=filters_dict.get('curated', DEFAULT_CURATED))


def _create_slack_config(slack_dict: Dict) -> SlackConfig:
    """Create SlackConfig object from a dictionary."""
    return SlackConfig(
        users=slack_dict.get('users', []),
        channels=slack_dict.get('channels', []))


def create_subscription_from_dict(subscription_dict: Dict) -> Subscription:
    """Create Subscription object from dictionary.

    Args:
        subscription_dict: Dictionary containing subscription information
    Returns:
        Subscription object
    Raises:
        MissingSubscriptionsError: If subscription_dict is empty
        InvalidSubscriptionError: If required fields are missing
    """

    if not subscription_dict:
        raise MissingSubscriptionsError()

    required_fields = ['subscription_type', 'id', 'query']
    for f in required_fields:
        if f not in subscription_dict:
            subscription_id = subscription_dict.get('id')
            if subscription_id:
                raise InvalidSubscriptionError(f'Subscription ID `{subscription_id}` '
                                               f'missing required field: {f}')
            else:
                raise InvalidSubscriptionError(f'Missing required field: {f}')


    filters = _create_filters(subscription_dict.get('filters', {}))
    slack_destinations = None
    if subscription_dict.get('slack_destinations'):
        slack_destinations = _create_slack_config(subscription_dict.get('slack_destinations'))

    return Subscription(
        subscription_type=subscription_dict.get('subscription_type'),
        id=subscription_dict.get('id'),
        query=subscription_dict.get('query'),
        filters=filters,
        slack_destinations=slack_destinations)
