"""Model that contains configuration settings for Talkback Messenger.

Typical usage example:
    from talkback_messenger.models import config
    config = config.create_config_from_dict(config_dict)
"""

from dataclasses import dataclass
from typing import List, Optional

from talkback_messenger.models import subscription
from talkback_messenger.models.utils import validate_fields


@dataclass(slots=True)
class SlackDefaults:
    """Slack defaults for the application"""
    default_user: Optional[str]
    default_channel: str


@dataclass(slots=True)
class Config:
    """Configuration for the application"""
    slack_defaults: Optional[SlackDefaults]
    subscriptions: List[subscription.Subscription]

    def __post_init__(self):
        validate_fields(self, {
            'subscriptions': list
        })


def create_config_from_dict(config_dict: dict) -> Config:
    """Create Config object from dictionary"""

    if config_dict.get('slack'):
        slack_config = SlackDefaults(
            default_user=config_dict.get('slack').get('default_user'),
            default_channel=config_dict.get('slack').get('default_channel')
        )
    else:
        slack_config = None

    return Config(
        slack_defaults=slack_config,
        subscriptions=config_dict.get('subscriptions', [])
    )
