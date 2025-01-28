import pytest

from fixtures import mock_subscription
from talkback_messenger.models import subscription
from talkback_messenger.exceptions import InvalidSubscriptionError, MissingSubscriptionsError


# Base Test: Ensure the Subscription object initializes correctly
def test_subscription_initialisation(mock_subscription):
    assert isinstance(mock_subscription, subscription.Subscription)

    # Validate attributes
    assert mock_subscription.subscription_type == 'category'
    assert mock_subscription.query == 'cloud security'
    assert mock_subscription.filters.rank == 20
    assert mock_subscription.filters.resource_types == ['post', 'news']
    assert mock_subscription.slack_destinations.users == ['tobias.funke@example.com']
    assert mock_subscription.slack_destinations.channels == ['C01234567']


# Test missing optional fields
def test_subscription_creation_missing_fields():
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'firefox',
        'query': 'firefox'
    }

    mock_subscription = subscription.create_subscription_from_dict(subscription_dict)

    assert isinstance(mock_subscription, subscription.Subscription)
    assert mock_subscription.subscription_type == 'category'
    assert mock_subscription.query == 'firefox'
    assert mock_subscription.filters.rank == 80.00
    assert mock_subscription.filters.resource_types == [
        'post', 'news', 'oss', 'video', 'paper', 'slides', 'n_a']
    assert not mock_subscription.filters.curated
    assert mock_subscription.slack_destinations is None


# Test invalid rank value
def test_subscription_creation_invalid_rank():
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
    assert subscription_object.filters.rank == 80.00  # Default rank applied


# Test invalid field types
def test_subscription_creation_incorrect_field_type():
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


# Test edge case: Empty filters
def test_subscription_creation_empty_filters():
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'edge-case',
        'query': 'test',
        'filters': {}
    }

    subscription_object = subscription.create_subscription_from_dict(subscription_dict)

    assert subscription_object.filters.rank == 80.00
    assert subscription_object.filters.resource_types == [
        'post', 'news', 'oss', 'video', 'paper', 'slides', 'n_a']
    assert not subscription_object.filters.curated


# Test boundary rank values
def test_subscription_creation_boundary_rank():
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'boundary-case',
        'query': 'test',
        'filters': {
            'rank': 0
        }
    }

    subscription_object = subscription.create_subscription_from_dict(subscription_dict)

    assert subscription_object.filters.rank == 0  # Boundary value


# Test empty Slack config
def test_subscription_creation_empty_slack_config():
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'empty-slack',
        'query': 'test',
        'slack_destinations': {}
    }

    subscription_object = subscription.create_subscription_from_dict(subscription_dict)

    assert not subscription_object.slack_destinations


# Test partial Slack config
def test_subscription_creation_partial_slack_config():
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'partial-slack',
        'query': 'test',
        'slack_destinations': {
            'users': ['test.user@example.com']
        }
    }

    subscription_object = subscription.create_subscription_from_dict(subscription_dict)

    assert subscription_object.slack_destinations.users == ['test.user@example.com']
    assert subscription_object.slack_destinations.channels == []  # Default empty list


# Test invalid subscription type
def test_subscription_creation_invalid_subscription_type():
    subscription_dict = {
        'subscription_type': 123,  # Invalid type
        'id': 'invalid-type',
        'query': 'test'
    }

    with pytest.raises(TypeError):
        subscription.create_subscription_from_dict(subscription_dict)


# Test invalid filters and Slack config together
def test_subscription_creation_invalid_filters_and_slack_config():
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'invalid-combo',
        'query': 'test',
        'filters': {
            'rank': 'invalid-rank',
            'resource_types': 123,
        },
        'slack_destinations': {
            'users': 123,
            'channels': 'not-a-list'
        }
    }

    with pytest.raises(TypeError):
        subscription.create_subscription_from_dict(subscription_dict)


# Test full input
def test_subscription_creation_full_input():
    subscription_dict = {
        'subscription_type': 'category',
        'id': 'full-input',
        'query': 'test query',
        'filters': {
            'rank': 90.0,
            'resource_types': ['video', 'paper'],
            'curated': True
        },
        'slack_destinations': {
            'users': ['john.doe@example.com', 'jane.doe@example.com'],
            'channels': ['C01234567', 'C07654321']
        }
    }

    subscription_object = subscription.create_subscription_from_dict(subscription_dict)

    assert subscription_object.subscription_type == 'category'
    assert subscription_object.id == 'full-input'
    assert subscription_object.query == 'test query'
    assert subscription_object.filters.rank == 90.0
    assert subscription_object.filters.resource_types == ['video', 'paper']
    assert subscription_object.filters.curated is True
    assert subscription_object.slack_destinations.users == ['john.doe@example.com', 'jane.doe@example.com']
    assert subscription_object.slack_destinations.channels == ['C01234567', 'C07654321']


# Test empty input
def test_subscription_creation_empty_input():
    subscription_dict = {}

    with pytest.raises(MissingSubscriptionsError):
        subscription.create_subscription_from_dict(subscription_dict)


# Test missing required fields
def test_subscription_creation_missing_required_fields():
    subscription_dict = {
        'id': 'missing-fields',
        'query': None
    }

    with pytest.raises(InvalidSubscriptionError):
        subscription.create_subscription_from_dict(subscription_dict)
