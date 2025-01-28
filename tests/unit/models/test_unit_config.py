from fixtures import mock_config, mock_subscription
from talkback_messenger.models import config


def test_config_initialisation(mock_config):
    # Test that the Config object is initialised correctly
    assert isinstance(mock_config, config.Config)

    # Test that the config object has the correct attributes
    assert mock_config.slack_defaults.default_user == 'tobias.funke@example.com'
    assert mock_config.slack_defaults.default_channel == 'C01234567'
    assert len(mock_config.subscriptions) == 1


def test_config_creation_missing_fields(mock_subscription):
    # Test that a Config object is created correctly with missing fields
    config_dict = {
        'subscriptions': [mock_subscription]
    }

    mock_config = config.create_config_from_dict(config_dict)

    assert isinstance(mock_config, config.Config)

    assert mock_config.slack_defaults is None
    assert len(mock_config.subscriptions) == 1
    assert mock_config.subscriptions[0] == mock_subscription