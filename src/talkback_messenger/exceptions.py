class NoConfigFoundError(Exception):
    """Raised when no config file is found"""

    def __init__(self):
        self.message = '''
        No config file found. Please provide a path to a talkback.conf file using the --config argument.
        If you are running the app in a container, make sure to mount the config file
        at /etc/talkback-messenger/talkback.conf
        '''
        super().__init__(self.message)


class NoDestinationError(Exception):
    """Raised when no destination is provided"""

    def __init__(self, subscription):
        self.message = (f'No destination provided for the subscription {subscription.category} - {subscription.name}.'
                        f' Please provide a destination for the message')
        super().__init__(self.message)
