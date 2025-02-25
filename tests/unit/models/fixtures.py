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

    # MOCK_RESOURCE = {
    #     'id': '6eb4741f-285d-4235-806f-73673ee0cd00',
    #     'url': 'https://posts.specterops.io/intune-attack-paths-part-1-4ad1882c1811',
    #     'type': 'POST',
    #     'createdDate': '2025-01-15T17:33:08+00:00',
    #     'title': 'Intune Attack Paths Part 1',
    #     'domain': {
    #         'name': 'specterops.io'
    #     },
    #     'curators': [
    #         'tl;drsec'
    #     ],
    #     'categories': [
    #         {
    #             'fullname': 'cloud security'
    #         }
    #     ],
    #     'rank': '99.03',
    #     'tier': 4,
    #     'readtime': 14,
    #     'synopsis': 'Intune is a Microsoft service for endpoint management, targeted by adversaries for its privileged actions, with Entra tenant establishing trust boundaries and RBAC systems for control and management of devices.',
    #     'summary': [
    #         'Intune is a Microsoft service for endpoint management, with efforts being made to transition users from other systems like SCCM to Intune.',
    #         'Intune is an attractive target for adversaries due to its capabilities to perform highly privileged actions on endpoints.',
    #         'The trust boundary around an Intune instance is established and enforced by the Entra tenant, with specific roles granting full control of an Intune instance.',
    #         'Intune devices are distinct from Entra devices, managed through separate APIs and identified by unique identifiers.',
    #         'Intune utilizes RBAC systems for role assignments, permissions, and scope groups, with mechanisms to limit control to specific sets of endpoints.'],
    #     'topics': [
    #         {
    #             'name': 'Intune',
    #             'vendor': {
    #                 'name': 'Microsoft',
    #             },
    #             'type': 'Endpoint management service',
    #             'url': 'https://example.com/intune'
    #         }
    #     ],
    #     'vulnerabilities': [
    #         {
    #             'name': 'CVE-2023-1234',
    #             'cvss': '9.8',
    #             'cwes': ['CWE-123'],
    #             'url': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1234'
    #         }
    #     ],
    #     'vendors': [
    #         'Microsoft'
    #     ]
    # }

    MOCK_RESOURCE = {
        "id": "e70e07ae-3191-4b80-85de-842a0ba64e08",
        "url": "https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/three-years-of-cyber-warfare-how-digital-attacks-have-shaped-the-russia-ukraine-war/",
        "type": "POST",
        "cves": [
            {
                "id": "CVE-2023-0669",
                "status": "Modified",
                "publishedDate": "2023-02-06T20:15:14.300000+00:00",
                "modifiedDate": "2024-11-21T07:37:35.710000+00:00",
                "description": "Fortra (formerly, HelpSystems) GoAnywhere MFT suffers from a pre-authentication command injection vulnerability in the License Response Servlet due to deserializing an arbitrary attacker-controlled object. This issue was patched in version 7.1.2.",
                "cwes": [
                    {
                        "id": "CWE-502",
                        "name": "Deserialization of Untrusted Data"
                    }
                ]
            },
            {
                "id": "CVE-2023-34362",
                "status": "Undergoing Analysis",
                "publishedDate": "2023-06-02T14:15:09.487000+00:00",
                "modifiedDate": "2024-11-21T08:07:05.843000+00:00",
                "description": "In Progress MOVEit Transfer before 2021.0.6 (13.0.6), 2021.1.4 (13.1.4), 2022.0.4 (14.0.4), 2022.1.5 (14.1.5), and 2023.0.1 (15.0.1), a SQL injection vulnerability has been found in the MOVEit Transfer web application that could allow an unauthenticated attacker to gain access to MOVEit Transfer's database. Depending on the database engine being used (MySQL, Microsoft SQL Server, or Azure SQL), an attacker may be able to infer information about the structure and contents of the database, and execute SQL statements that alter or delete database elements. NOTE: this is exploited in the wild in May and June 2023; exploitation of unpatched systems can occur via HTTP or HTTPS. All versions (e.g., 2020.0 and 2019x) before the five explicitly mentioned versions are affected, including older unsupported versions.",
                "cwes": [
                    {
                        "id": "CWE-89",
                        "name": "Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')"
                    }
                ]
            }
        ],
        "summary": [
            "Trustwave SpiderLabs created a series of blog posts reflecting on the Russia-Ukraine war, highlighting the cyber warfare aspect fought beyond national boundaries.",
            "The series examines various threat groups involved, their tactics, malware, and targets in sectors like technology and critical infrastructure.",
            "Key findings include details on cyber warfare groups supporting Ukraine like Core Werewolf and Sticky Werewolf, as well as Russian groups like Sandworm and APT44.",
            "Russian cyber operations against Ukraine involve APT groups conducting disruptive attacks, data theft, and espionage under state sponsorship.",
            "Russian cyberattacks are characterized by scale, coordination, technical sophistication, dual-purpose strategies, and methods like critical infrastructure attacks, data exfiltration, destructive malware, ransomware campaigns, DDoS attacks, and phishing."
        ],
        "synopsis": "Trustwave SpiderLabs analyzes cyber warfare dynamics in the Russia-Ukraine conflict, detailing threat groups, tactics, and targets, including state-sponsored Russian cyber operations and Ukrainian-supported groups like Core Werewolf and Sticky Werewolf.",
        "topics": [
            {
                "url": "https://www.trustwave.com/en-us/spiderlabs",
                "name": "SpiderLabs",
                "type": "Cybersecurity Research and Consulting",
                "vendor": {
                    "name": "Trustwave SpiderLabs"
                }
            }
        ],
        "createdDate": "2025-02-20T21:52:41+00:00",
        "title": "Three Years of Cyber Warfare: How Digital Attacks Have Shaped the Russia-Ukraine War",
        "domain": {
            "name": "trustwave.com"
        },
        "curators": ['tl;drsec'],
        "categories": [
            {
                "fullname": "network security"
            },
            {
                "fullname": "malware analysis"
            }
        ],
        "rank": "86.37",
        "tier": 4,
        "readtime": 4
    }

    MOCK_TOPIC = {
        "url": "https://www.trustwave.com/en-us/spiderlabs",
        "name": "SpiderLabs",
        "type": "Cybersecurity Research and Consulting",
        "vendor": {
            "name": "Trustwave SpiderLabs"
        }
    }

    MOCK_VULNERABILITY = {
        "id": "CVE-2023-34362",
        "status": "Undergoing Analysis",
        "publishedDate": "2023-06-02T14:15:09.487000+00:00",
        "modifiedDate": "2024-11-21T08:07:05.843000+00:00",
        "description": "In Progress MOVEit Transfer before 2021.0.6 (13.0.6), 2021.1.4 (13.1.4), 2022.0.4 (14.0.4), 2022.1.5 (14.1.5), and 2023.0.1 (15.0.1), a SQL injection vulnerability has been found in the MOVEit Transfer web application that could allow an unauthenticated attacker to gain access to MOVEit Transfer's database. Depending on the database engine being used (MySQL, Microsoft SQL Server, or Azure SQL), an attacker may be able to infer information about the structure and contents of the database, and execute SQL statements that alter or delete database elements. NOTE: this is exploited in the wild in May and June 2023; exploitation of unpatched systems can occur via HTTP or HTTPS. All versions (e.g., 2020.0 and 2019x) before the five explicitly mentioned versions are affected, including older unsupported versions.",
        "cwes": [
            {
                "id": "CWE-89",
                "name": "Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')"
            }
        ]
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
    return resource.create_vulnerability_from_dict([MockData.MOCK_VULNERABILITY])
