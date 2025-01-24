import pytest

from fixtures import mock_subscription
from talkback_messenger.models import subscription

def test_subscription_initialisation(mock_subscription):
    # Test that the Subscription object is initialised correctly
    assert isinstance(mock_subscription, subscription.Subscription)

    # Test that the subscription object has the correct attributes
    assert mock_subscription.subscription_type == 'category'
    assert mock_subscription.query == 'cloud security'
    assert mock_subscription.filters.rank == 20
    assert mock_subscription.filters.resource_types == ['post', 'news']
    assert mock_subscription.slack_destinations.users == ['tobias.funke@example.com']
    assert mock_subscription.slack_destinations.channels == ['C01234567']


def test_subscription_creation_missing_fields():
    # Test that a Subscription object is created correctly with missing fields
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'firefox',
        'query': 'firefox'
    }

    mock_subscription = subscription.create_subscription_from_dict(subscription_dict)

    assert isinstance(mock_subscription, subscription.Subscription)

    # Test default values are set correctly
    assert mock_subscription.subscription_type == 'category'
    assert mock_subscription.query == 'firefox'
    assert mock_subscription.filters.rank == 80.00
    assert mock_subscription.filters.resource_types == ['post', 'news', 'oss', 'video', 'paper', 'slides', 'n_a']
    assert not mock_subscription.filters.curated

    # Slack config should be None
    assert not mock_subscription.slack_destinations


def test_subscription_creation_invalid_rank():
    # Test that a Subscription object is created correctly with invalid rank
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'firefox',
        'query': 'firefox',
        'filters': {
            'rank': 'invalid'
        }
    }

    subscription_object = subscription.create_subscription_from_dict(subscription_dict)

    assert isinstance(subscription_object, subscription.Subscription)

    # Test rank is correctly set to its default value
    assert subscription_object.filters.rank == 80.00

def test_subscription_creation_incorrect_field_type():
    # Test that a Subscription object is created correctly with incorrect field type
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'firefox',
        'query': 'firefox',
        'filters': {
            'rank': 'invalid',
            'resource_types': 'post',
            'curated': 'True'
        },
        'slack_destinations': {
            'users': 123,
            'channels': 123
        }
    }

    with pytest.raises(TypeError):
        subscription.create_subscription_from_dict(subscription_dict)