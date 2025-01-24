"""Model that contains configuration settings for Talkback Messenger.

Typical usage example:
    from talkback_messenger.models import config
    config = config.create_config_from_dict(config_dict)
"""

from dataclasses import dataclass
from typing import List, Optional

from talkback_messenger.models import subscription


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
        """Validate types of fields after initialisation."""
        expected_types = {
            'subscriptions': list
        }

        for field_name, expected_type in expected_types.items():
            value = getattr(self, field_name)
            if value is not None and not isinstance(value, expected_type):
                raise TypeError(
                    f'Expected `{field_name}` to be of type {expected_type}, '
                    f'received {type(value).__name__}'
                )


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
