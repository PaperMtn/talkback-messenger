from datetime import datetime

from fixtures import MockData, mock_resource, mock_vulnerability, mock_topic
from talkback_messenger.models import resource


def test_resource_initialisation(mock_resource, mock_topic, mock_vulnerability):
    # Test that the resource object is initialised correctly
    assert isinstance(mock_resource, resource.Resource)

    # Test that the resource object has the correct attributes
    assert mock_resource.id == 'e70e07ae-3191-4b80-85de-842a0ba64e08'
    assert mock_resource.url == 'https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/three-years-of-cyber-warfare-how-digital-attacks-have-shaped-the-russia-ukraine-war/'
    assert mock_resource.talkback_url == 'https://talkback.sh/resource/e70e07ae-3191-4b80-85de-842a0ba64e08'
    assert mock_resource.type == 'post'
    assert mock_resource.created_date == datetime.fromisoformat(MockData.MOCK_RESOURCE.get('createdDate'))
    assert mock_resource.title == 'Three Years of Cyber Warfare: How Digital Attacks Have Shaped the Russia-Ukraine War'
    assert mock_resource.domain == 'trustwave.com'
    assert mock_resource.curators == ['tl;drsec']
    assert mock_resource.categories == ['network security', 'malware analysis']
    assert mock_resource.rank == 86.37
    assert mock_resource.tier == 4
    assert mock_resource.synopsis == 'Trustwave SpiderLabs analyzes cyber warfare dynamics in the Russia-Ukraine conflict, detailing threat groups, tactics, and targets, including state-sponsored Russian cyber operations and Ukrainian-supported groups like Core Werewolf and Sticky Werewolf.'
    assert mock_resource.summary == [
            "Trustwave SpiderLabs created a series of blog posts reflecting on the Russia-Ukraine war, highlighting the cyber warfare aspect fought beyond national boundaries.",
            "The series examines various threat groups involved, their tactics, malware, and targets in sectors like technology and critical infrastructure.",
            "Key findings include details on cyber warfare groups supporting Ukraine like Core Werewolf and Sticky Werewolf, as well as Russian groups like Sandworm and APT44.",
            "Russian cyber operations against Ukraine involve APT groups conducting disruptive attacks, data theft, and espionage under state sponsorship.",
            "Russian cyberattacks are characterized by scale, coordination, technical sophistication, dual-purpose strategies, and methods like critical infrastructure attacks, data exfiltration, destructive malware, ransomware campaigns, DDoS attacks, and phishing."
        ]
    assert mock_resource.topics == [mock_topic]
    assert mock_resource.vendors == ['Trustwave SpiderLabs']

    # Test vulnerability details
    assert mock_resource.vulnerabilities[0].id == 'CVE-2023-0669'
    assert mock_resource.vulnerabilities[0].status == 'Modified'
    assert mock_resource.vulnerabilities[0].cwes[0]['id'] == 'CWE-502'
    assert mock_resource.vulnerabilities[1].id == 'CVE-2023-34362'
    assert mock_resource.vulnerabilities[1].status == 'Undergoing Analysis'
    assert mock_resource.vulnerabilities[1].cwes[0]['id'] == 'CWE-89'


def test_resource_initialisation_missing_fields():
    # Create a resource object with missing fields
    resource_dict = {
        'id': '6eb4741f-285d-4235-806f-73673ee0cd00',
        'url': 'https://posts.specterops.io/intune-attack-paths-part-1-4ad1882c1811',
        'type': 'POST',
    }
    mock_resource = resource.create_resource_from_dict(resource_dict)

    # Test that the resource object is initialised correctly
    assert isinstance(mock_resource, resource.Resource)

    # Test that the resource object has the correct attributes
    assert mock_resource.id == '6eb4741f-285d-4235-806f-73673ee0cd00'
    assert mock_resource.url == 'https://posts.specterops.io/intune-attack-paths-part-1-4ad1882c1811'
    assert mock_resource.type == 'post'
    assert isinstance(mock_resource.created_date, datetime)
    assert mock_resource.title is None
    assert mock_resource.domain is None
    assert mock_resource.curators is None
    assert mock_resource.categories == []
    assert mock_resource.rank is None
    assert mock_resource.tier is None
    assert mock_resource.synopsis is None
    assert mock_resource.summary is None
    assert mock_resource.topics == []
    assert mock_resource.vulnerabilities == []
    assert mock_resource.vendors == []

