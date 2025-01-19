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


@dataclass(slots=True)
class Subscription:
    """Subscription for Talkback resources"""
    subscription_type: str
    name: str
    rank: Union[int, float]
    resource_types: List[str]
    curated: bool
    slack_destinations: Optional[SlackConfig]

    def __post_init__(self):
        """Validate types of fields after initialisation."""
        expected_types = {
            'subscription_type': str,
            'name': str,
            'rank': Union[int, float],
            'resource_types': list,
            'curated': bool
        }

        for field, expected_type in expected_types.items():
            if not isinstance(getattr(self, field), expected_type):
                raise TypeError(f"Expected {field} to be of type {expected_type}")


def create_subscription_from_dict(subscription_dict: Dict) -> Subscription:
    """Create Subscription object from dictionary"""
    try:
        rank = float(subscription_dict.get('rank', 80.00))
    except (ValueError, TypeError):
        rank = 80.00

    if subscription_dict.get('slack'):
        slack_config = SlackConfig(
            users=subscription_dict.get('slack').get('users'),
            channels=subscription_dict.get('slack').get('channels')
        )
    else:
        slack_config = None

    return Subscription(
        subscription_type=subscription_dict.get('subscription_type'),
        name=subscription_dict.get('name'),
        rank=rank,
        resource_types=subscription_dict.get(
            'types',
            ['post', 'news', 'oss', 'video', 'paper', 'slides', 'n_a']),
        curated=subscription_dict.get('curated', False),
        slack_destinations=slack_config
    )
