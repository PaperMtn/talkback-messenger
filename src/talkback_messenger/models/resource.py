"""Resource model for Talkback API

Typical usage example:
    from talkback_messenger.models import resource
    res = resource.create_resource_from_dict(resource_dict)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Union


@dataclass(slots=True)
class Topic:
    """Topic from Talkback"""
    title: str
    vendor: str
    type: str


@dataclass(slots=True)
class Vulnerability:
    """Vulnerability from Talkback"""
    name: str
    cvss: str
    cwes: List[str]
    url: str


# pylint: disable=too-many-instance-attributes
@dataclass(slots=True)
class Resource:
    """Resource from Talkback"""
    id: str
    url: str
    talkback_url: str
    type: str
    created_date: datetime
    title: str
    domain: str
    curators: List[str]
    categories: List[str]
    rank: Union[int, float, str]
    tier: int
    readtime: int
    synopsis: str
    summary: List[str]
    topics: List[Topic]
    vulnerabilities: List[Vulnerability]
    vendors: List[str]

    def __post_init__(self):
        """Validate types of fields after initialisation."""
        expected_types = {
            'id': str,
            'url': str,
            'talkback_url': str,
            'type': str,
            'created_date': datetime,
            'title': str,
            'domain': str,
            'curators': list,
            'categories': list,
            'rank': Union[int, float, str],
            'tier': int,
            'readtime': int,
            'synopsis': str,
            'summary': list,
            'topics': list,
            'vulnerabilities': list,
            'vendors': list
        }

        for field_name, expected_type in expected_types.items():
            value = getattr(self, field_name)
            if value is not None and not isinstance(value, expected_type):
                raise TypeError(
                    f'Expected `{field_name}` to be of type {expected_type}, '
                    f'received {type(value).__name__}'
                )


def create_resource_from_dict(resource_dict: Dict) -> Resource:
    """ Create a Resource object

    Args:
        resource_dict: dict containing post information from the Talkback API
    Returns:
        Resource object
    """
    topics = [Topic(**topic) for topic in resource_dict.get('topics', [])]
    vulnerabilities = [Vulnerability(**vuln) for vuln in resource_dict.get('vulnerabilities', [])]

    return Resource(
        id=resource_dict.get('id'),
        url=resource_dict.get('url'),
        talkback_url=f'https://talkback.sh/resource/{resource_dict.get("id")}',
        type=resource_dict.get('type', '').lower(),
        created_date=datetime.fromisoformat(resource_dict.get('createdDate', '2020-01-01T00:00:00+00:00')),
        title=resource_dict.get('title'),
        domain=resource_dict.get('domain', {}).get('name'),
        curators=resource_dict.get('curators'),
        categories=[category.get('fullname') for category in resource_dict.get('categories', [])],
        rank=float(resource_dict.get('rank')) if resource_dict.get('rank') else None,
        tier=resource_dict.get('tier'),
        readtime=resource_dict.get('readtime'),
        synopsis=resource_dict.get('synopsis'),
        summary=resource_dict.get('summary'),
        topics=topics,
        vulnerabilities=vulnerabilities,
        vendors=resource_dict.get('vendors', []),
    )
