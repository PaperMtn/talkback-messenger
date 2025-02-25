"""Module to build Slack Block Kit formatted messages from Talkback resources

This module contains functions to build Slack Block Kit formatted messages for
the initial Slack post, and then for the post in the thread that proceeds it.

Typical usage example:
    slack_post = build_slack_post(resource)
    thread_message = build_thread_message(resource, subscription)
"""

from typing import List, Dict, Any

from talkback_messenger.models.resource import Resource
from talkback_messenger.models.subscription import Subscription


def build_slack_post(resource: Resource) -> List[Dict[Any, Any]]:
    """Build blocks for a Slack post from a Talkback resource

    Args:
        resource (Resource): Talkback resource
    Returns:
        Dict: Block kit formatted Slack post
    """

    category_list = [c.title() for c in resource.categories]
    categories = '\n• '.join(category_list)
    topics = '\n• '.join([topic.name for topic in resource.topics])
    vendors_list = [v for v in resource.vendors if v]
    vendors = '\n• '.join(vendors_list)

    if resource.type == 'oss':
        resource.type = 'Open Source Software'

    created_date = resource.created_date.strftime('%Y-%m-%d %H:%M:%S')

    if len(resource.title) > 150:
        header = {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'*{resource.title}*:'
            }
        }
    else:
        header = {
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': resource.title
            }
        }

    message_template = [
        header,
        {
            'type': 'section',
            'fields': [
                {
                    'type': 'mrkdwn',
                    'text': f':page_with_curl:* Resource Type*: {resource.type.title()}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f':book:* Time to read*: {resource.readtime} mins'
                },
                {
                    'type': 'mrkdwn',
                    'text': f':clock1: *Indexed*: `{created_date}`'

                },
                {
                    'type': 'mrkdwn',
                    'text': f':card_index_dividers: *Categories*:\n• {categories}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f':link: *Source*: `{resource.domain.replace('.', '[.]')}`'
                }
            ]
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'*Resource Link*: <{resource.url}|{resource.url}>'
            }
        },
        {
            'type': 'section',
            'fields': [
                {
                    'type': 'mrkdwn',
                    'text': f':pushpin: *Topics*:\n• {topics}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f':card_index: *Vendors*:\n• {vendors}'
                }
            ]
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '*AI Synopsis*:'
            }
        },
        {
            'type': 'rich_text',
            'elements': [
                {
                    'type': 'rich_text_quote',
                    'elements': [
                        {
                            'type': 'text',
                            'text': f'{resource.synopsis}',
                            'style': {
                                'italic': True
                            }
                        }
                    ]
                }
            ]
        }
    ]
    return message_template


def build_thread_message(resource: Resource, subscription: Subscription) -> List[Dict[Any, Any]]:
    """Build blocks for a thread message for the Talkback slack post

    Args:
        resource (Resource): Talkback resource
        subscription (Subscription): Subscription object
    Returns:
        Dict: Block kit formatted Slack thread message
    """

    summary_elements = []
    for line in resource.summary:
        summary_elements.append(
            {
                'type': 'text',
                'text': line,
                'style': {
                    'italic': True
                }
            })
        summary_elements.append(
            {
                'type': 'text',
                'text': '\n\n'
            },
        )

    message_template = [
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '*AI Summary*:'
            }
        },
        {
            'type': 'rich_text',
            'elements': [
                {
                    'type': 'rich_text_quote',
                    'elements': summary_elements
                }
            ]
        },
        {
            'type': 'context',
            'elements': [
                {
                    'type': 'mrkdwn',
                    'text': f'*Meta:* \nTalkback URL: <{resource.talkback_url}|{resource.talkback_url}>'
                            f'\nRank: `{resource.rank}`\nSubscription: `{subscription.subscription_type}: '
                            f'{subscription.query}`'
                }
            ]
        }
    ]

    if resource.vulnerabilities:
        vulnerabilities = [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '*Vulnerabilities Referenced*:'
            }
        }]
        vuln_elements = []
        for vuln in resource.vulnerabilities:
            vuln_elements.append(
                {
                    'type': 'rich_text_section',
                    'elements': [
                        {
                            'type': 'link',
                            'url': f'https://talkback.sh/vulnerability/{vuln.id}/',
                            'text': vuln.id,
                            'style': {
                                'bold': True
                            }
                        }
                    ]
                }
            )

        vulnerabilities.append({
            'type': 'rich_text',
            'elements': [
                {
                    'type': 'rich_text_list',
                    'style': 'bullet',
                    'indent': 0,
                    'elements': vuln_elements
                }
            ]
        })
        for m in vulnerabilities:
            message_template.insert(-1, m)
    return message_template
