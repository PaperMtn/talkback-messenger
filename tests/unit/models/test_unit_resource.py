from datetime import datetime

from fixtures import MockData, mock_resource, mock_vulnerability, mock_topic
from talkback_messenger.models import resource


def test_resource_initialisation(mock_resource, mock_topic, mock_vulnerability):
    # Test that the resource object is initialised correctly
    assert isinstance(mock_resource, resource.Resource)

    # Test that the resource object has the correct attributes
    assert mock_resource.id == '6eb4741f-285d-4235-806f-73673ee0cd00'
    assert mock_resource.url == 'https://posts.specterops.io/intune-attack-paths-part-1-4ad1882c1811'
    assert mock_resource.talkback_url == 'https://talkback.sh/resource/6eb4741f-285d-4235-806f-73673ee0cd00'
    assert mock_resource.type == 'post'
    assert mock_resource.created_date == datetime.fromisoformat(MockData.MOCK_RESOURCE.get('createdDate'))
    assert mock_resource.title == 'Intune Attack Paths Part 1'
    assert mock_resource.domain == 'specterops.io'
    assert mock_resource.curators == ['tl;drsec']
    assert mock_resource.categories == ['cloud security']
    assert mock_resource.rank == 99.03
    assert mock_resource.tier == 4
    assert mock_resource.synopsis == 'Intune is a Microsoft service for endpoint management, targeted by adversaries for its privileged actions, with Entra tenant establishing trust boundaries and RBAC systems for control and management of devices.'
    assert mock_resource.summary == [
        'Intune is a Microsoft service for endpoint management, with efforts being made to transition users from other systems like SCCM to Intune.',
        'Intune is an attractive target for adversaries due to its capabilities to perform highly privileged actions on endpoints.',
        'The trust boundary around an Intune instance is established and enforced by the Entra tenant, with specific roles granting full control of an Intune instance.',
        'Intune devices are distinct from Entra devices, managed through separate APIs and identified by unique identifiers.',
        'Intune utilizes RBAC systems for role assignments, permissions, and scope groups, with mechanisms to limit control to specific sets of endpoints.'
    ]
    assert mock_resource.topics == [mock_topic]
    assert mock_resource.vulnerabilities == [mock_vulnerability]
    assert mock_resource.vendors == ['Microsoft']


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

