import copy

import pytest

from talkback_messenger.models import config, subscription, resource


class MockData:
    MOCK_CONFIG = {
        'slack': {
            'default_channel': 'C01234567',
            'default_user': 'tobias.funke@example.com'
        },
        'subscriptions': {
            'sources': [
                {
                    'query': 'papermtn.co.uk',
                    'id': 'Papermtn',
                    'filters': {
                        'rank': 60
                    }
                },
                {
                    'query': 'github.com/PaperMtn',
                    'id': 'GitHub PaperMtn',
                    'filters': {
                        'rank': 20
                    }
                }
            ],
            'vendors': [
                {
                    'query': 'google',
                    'id': 'Google',
                    'filters': {
                        'rank': 20
                    }
                }
            ],
            'queries': [
                {
                    'query': 'title:slack',
                    'id': 'Slack Posts',
                    'filters': {
                        'resource_types': [
                            'post',
                            'oss'
                        ],
                        'rank': 50
                    }
                }
            ],
            'vulnerabilities': [
                {
                    'query': 'CVE-2023-1234',
                    'id': 'CVE-2023-1234',
                    'filters': {
                        'resource_types': [
                            'post',
                            'news'
                        ],
                        'rank': 20
                    }
                }
            ],
            'topics': [
                {
                    'query': 'chrome',
                    'id': 'Chrome',
                    'filters': {
                        'rank': 20
                    }
                },
                {
                    'query': 'firefox',
                    'id': 'Firefox',
                    'filters': {
                        'rank': 20
                    }
                }
            ],
            'categories': [
                {
                    'query': 'application security',
                    'id': 'Application Security Posts',
                    'filters': {
                        'resource_types': [
                            'post',
                            'news'
                        ],
                        'curated': True,
                        'rank': 20
                    }
                },
                {
                    'query': 'cloud security',
                    'filters': {
                        'resource_types': [
                            'post',
                            'news'
                        ],
                        'rank': 20
                    },
                    'id': 'Cloud Security Posts',
                    'slack_destinations': {
                        'channels': [
                            'C01234567'
                        ],
                        'users': [
                            'tobias.funke@example.com'
                        ]
                    }
                }
            ]
        }
    }

    MOCK_SUBSCRIPTION = {
        'subscription_type': 'category',
        'id': 'Cloud Security Posts',
        'query': 'cloud security',
        'filters': {
            'resource_types': [
                'post',
                'news'
            ],
            'rank': 20
        },
        'slack_destinations': {
            'channels': [
                'C01234567'
            ],
            'users': [
                'tobias.funke@example.com'
            ]
        }
    }

    MOCK_RESOURCE = {
        'id': '6eb4741f-285d-4235-806f-73673ee0cd00',
        'url': 'https://posts.specterops.io/intune-attack-paths-part-1-4ad1882c1811',
        'type': 'POST',
        'createdDate': '2025-01-15T17:33:08+00:00',
        'title': 'Intune Attack Paths Part 1',
        'domain': {
            'name': 'specterops.io'
        },
        'curators': [
            'tl;drsec'
        ],
        'categories': [
            {
                'fullname': 'cloud security'
            }
        ],
        'rank': '99.03',
        'tier': 4,
        'readtime': 14,
        'synopsis': 'Intune is a Microsoft service for endpoint management, targeted by adversaries for its privileged actions, with Entra tenant establishing trust boundaries and RBAC systems for control and management of devices.',
        'summary': [
            'Intune is a Microsoft service for endpoint management, with efforts being made to transition users from other systems like SCCM to Intune.',
            'Intune is an attractive target for adversaries due to its capabilities to perform highly privileged actions on endpoints.',
            'The trust boundary around an Intune instance is established and enforced by the Entra tenant, with specific roles granting full control of an Intune instance.',
            'Intune devices are distinct from Entra devices, managed through separate APIs and identified by unique identifiers.',
            'Intune utilizes RBAC systems for role assignments, permissions, and scope groups, with mechanisms to limit control to specific sets of endpoints.'],
        'topics': [
            {
                'title': 'Intune',
                'vendor': 'Microsoft',
                'type': 'Endpoint management service'
            }
        ],
        'vulnerabilities': [
            {
                'name': 'CVE-2023-1234',
                'cvss': '9.8',
                'cwes': ['CWE-123'],
                'url': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1234'
            }
        ],
        'vendors': [
            'Microsoft'
        ]
    }

    MOCK_TOPIC = {
        'title': 'Intune',
        'vendor': 'Microsoft',
        'type': 'Endpoint management service'
    }

    MOCK_VULNERABILITY = {
        'name': 'CVE-2023-1234',
        'cvss': '9.8',
        'cwes': ['CWE-123'],
        'url': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1234'
    }


@pytest.fixture
def mock_subscription():
    return subscription.create_subscription_from_dict(MockData.MOCK_SUBSCRIPTION)


@pytest.fixture
def mock_config(mock_subscription):
    config_data = copy.deepcopy(MockData.MOCK_CONFIG)
    config_data['subscriptions'] = [mock_subscription]
    return config.create_config_from_dict(config_data)


@pytest.fixture
def mock_resource():
    return resource.create_resource_from_dict(MockData.MOCK_RESOURCE)


@pytest.fixture
def mock_topic():
    return resource.Topic(**MockData.MOCK_TOPIC)


@pytest.fixture
def mock_vulnerability():
    return resource.Vulnerability(**MockData.MOCK_VULNERABILITY)
