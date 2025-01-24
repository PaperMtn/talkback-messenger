"""Module for Subscription model

Typical usage example:
    from talkback_messenger.models import subscription
    sub = subscription.create_subscription_from_dict(subscription_dict)
"""

from dataclasses import dataclass
from typing import List, Dict, Union, Optional


@dataclass(slots=True)
class SlackConfig:
    """Slack users and channels to send messages to"""
    users: Optional[List[str]]
    channels: Optional[List[str]]

    def __post_init__(self):
        """Validate types of fields after initialisation."""
        expected_types = {
            'users': list,
            'channels': list
        }

        for field, expected_type in expected_types.items():
            if not isinstance(getattr(self, field), expected_type):
                raise TypeError(f"Expected {field} to be of type {expected_type}")

@dataclass(slots=True)
class Filters:
    """Filters to use with the subscription to narrow down resources"""
    rank: Optional[Union[int, float]]
    resource_types: Optional[List[str]]
    curated: Optional[bool]

    def __post_init__(self):
        """Validate types of fields after initialisation."""
        expected_types = {
            'rank': (int, float),
            'resource_types': list,
            'curated': bool
        }

        for field, expected_type in expected_types.items():
            if not isinstance(getattr(self, field), expected_type):
                raise TypeError(f"Expected {field} to be of type {expected_type}")

@dataclass(slots=True)
class Subscription:
    """Subscription for Talkback resources"""
    subscription_type: str
    id: str
    query: str
    filters: Filters
    slack_destinations: Optional[SlackConfig]

    def __post_init__(self):
        """Validate types of fields after initialisation."""
        expected_types = {
            'subscription_type': str,
            'id': str,
            'query': str
        }

        for field, expected_type in expected_types.items():
            if not isinstance(getattr(self, field), expected_type):
                raise TypeError(f"Expected {field} to be of type {expected_type}")


def create_subscription_from_dict(subscription_dict: Dict) -> Subscription:
    """Create Subscription object from dictionary"""

    if subscription_dict.get('filters'):
        try:
            rank = float(subscription_dict.get('filters').get('rank', 80.00))
        except (ValueError, TypeError):
            rank = 80.00

        filters = Filters(
            rank=rank,
            resource_types=subscription_dict.get('filters').get(
                'resource_types',
                ['post', 'news', 'oss', 'video', 'paper', 'slides', 'n_a']),
            curated=subscription_dict.get('curated', False))
    else:
        filters = Filters(
            rank=80.00,
            resource_types=['post', 'news', 'oss', 'video', 'paper', 'slides', 'n_a'],
            curated=False)

    if subscription_dict.get('slack_destinations'):
        slack_config = SlackConfig(
            users=subscription_dict.get('slack_destinations').get('users'),
            channels=subscription_dict.get('slack_destinations').get('channels'))
    else:
        slack_config = None

    return Subscription(
        subscription_type=subscription_dict.get('subscription_type'),
        id=subscription_dict.get('id'),
        query=subscription_dict.get('query'),
        filters=filters,
        slack_destinations=slack_config)
