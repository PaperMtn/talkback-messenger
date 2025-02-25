"""Custom exceptions for Talkback Messenger

Typical usage example:
    from talkback_messenger.exceptions import NoConfigFoundError

    raise NoConfigFoundError()
"""

class NoConfigFoundError(Exception):
    """Raised when no config file is found"""

    def __init__(self):
        self.message = '''
        No config file found. Please provide a path to a talkback.yml file using the --config argument.
        If you are running the app in a container, make sure to mount the config file
        at /etc/talkback-messenger/talkback.yml
        '''
        super().__init__(self.message)


class NoDestinationError(Exception):
    """Raised when no destination is provided

    Args:
        subscription: Subscription object
    """

    def __init__(self, subscription):
        self.message = (f'No destination provided for the subscription {subscription.category} - {subscription.query}.'
                        f' Please provide a destination for the message')
        super().__init__(self.message)


class InvalidSubscriptionError(Exception):
    """Raised when a subscription is configured incorrectly
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MissingSubscriptionsError(Exception):
    """Raised when subscriptions are missing from the configuration
    """

    def __init__(self):
        self.message = ('The configuration file is missing entries under the `subscriptions` key. Please '
                        'check the configuration file and ensure that the `subscriptions` key is present '
                        'with at least one subscription entry.')
        super().__init__(self.message)


class TalkbackAPIError(Exception):
    """Raised when the Talkback API returns an error

    Args:
        message: Error message
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TalkbackAuthenticationError(Exception):
    """Raised when the Talkback API authentication fails

    Args:
        message: Error message
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class MissingEnvVarError(Exception):
    """Exception raised when an environment variable is missing.

    Args:
        env_var: Name of the environment variable that is missing
    """

    def __init__(self, env_var):
        self.env_var = env_var
        self.message = f'Missing Environment Variable: {self.env_var}'
        super().__init__(self.message)
