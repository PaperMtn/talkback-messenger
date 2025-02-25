"""Core functionality for the Talkback Messenger bot

This module contains the core functionality for the Talkback Messenger bot.
This includes:
- Loading the application configuration
- Searching for resources in Talkback
- Filtering resources against subscriptions
- Sending Slack posts for found resources

Typical usage example:
    from talkback_messenger import talkback_bot_core
    app_config = await talkback_bot_core.load_app_config('talkback.yml')
    resources = await talkback_bot_core.get_subscribed_content(talkback_client, app_config.subscriptions)
    await talkback_bot_core.send_slack_posts(resources)
"""

import json
import re
from typing import List, Optional, Tuple

from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from talkback_messenger import slack_builder
from talkback_messenger.clients.talkback_client import TalkbackClient
from talkback_messenger.models import resource, subscription, config
from talkback_messenger.utils import load_config, deduplicate_results
from talkback_messenger.exceptions import (
    NoConfigFoundError,
    NoDestinationError,
    MissingSubscriptionsError,
    InvalidSubscriptionError
)


async def load_app_config(filepath: str) -> config.Config:
    """Load subscriptions from configuration file

    Args:
        filepath: Path to the configuration file
    Returns:
        List of Subscription objects
    """
    #TODO - Deal with incorrectly formatted config

    app_config = load_config(filepath)
    if not app_config:
        raise NoConfigFoundError()

    subscriptions = []
    subscription_types = {
        'category': 'categories',
        'topic': 'topics',
        'source': 'sources',
        'vulnerability': 'vulnerabilities',
        'query': 'queries',
        'vendor': 'vendors'
    }

    for sub_type, config_key in subscription_types.items():
        for sub in app_config.get('subscriptions').get(config_key, []):
            sub['subscription_type'] = sub_type
            try:
                subscriptions.append(subscription.create_subscription_from_dict(sub))
            except InvalidSubscriptionError as e:
                logger.error(f'Error creating subscription: {e}')
                continue
            except MissingSubscriptionsError as e:
                raise e
    talkback_config = config.Config(
        slack_defaults=config.SlackDefaults(
            default_user=app_config.get('slack').get('default_user'),
            default_channel=app_config.get('slack').get('default_channel')
        ),
        subscriptions=subscriptions
    )
    return talkback_config


async def find_resources(talkback_client: TalkbackClient,
                         search: str,
                         created_after: str,
                         created_before: Optional[str] = None) -> List[resource.Resource]:
    """Carry out a search query on Talkback and enrich the results with additional information.

    Args:
        talkback_client: TalkbackClient object
        search: Search query
        created_after: Created after date
        created_before: Created before date (optional)
    Returns:
        List of Resource objects
    """

    resources = await talkback_client.search_resources(
        search=search,
        created_after=created_after,
        created_before=created_before
    )
    # for res in resources:
    #     results.append(resource.create_resource_from_dict(res))

    return [resource.create_resource_from_dict(res) for res in resources]


# pylint: disable=too-many-return-statements
def filter_resource(res: resource.Resource, sub: subscription.Subscription) -> bool:
    """Filter a resource against a subscription

    Args:
        res: Resource object
        sub: Subscription object
    Returns:
        True if the resource matches the subscription, False otherwise
    """

    def _common_checks(r: resource.Resource, s: subscription.Subscription) -> bool:
        if r.rank < s.filters.rank:
            logger.debug(f'RANK - Resource `{r.title}` rank {r.rank} is lower than subscription '
                         f'`{s.subscription_type}: {s.query}` rank: {s.filters.rank}')
            return False
        if r.type not in s.filters.resource_types:
            logger.debug(f'TYPE - Resource `{r.title}` type {r.type} not in subscription '
                         f'`{s.subscription_type}: {s.query}` types {s.filters.resource_types}')
            return False
        if s.filters.curated and not r.curators:
            logger.debug(f'CURATION - Resource `{r.title}` is not curated, the subscription '
                         f'`{s.subscription_type}: {s.query}` requires curated resources')
            return False
        return True

    if not _common_checks(res, sub):
        return False

    if sub.subscription_type == 'query':
        return True
    elif sub.subscription_type == 'category':
        return sub.query.lower() in (r.lower() for r in res.categories)
    elif sub.subscription_type == 'topic':
        return sub.query.lower() in (r.name.lower() for r in res.topics)
    elif sub.subscription_type == 'source':
        return sub.query.lower() in res.domain.lower()
    elif sub.subscription_type == 'vendor':
        return sub.query.lower() in (r.lower() for r in res.vendors)
    elif sub.subscription_type == 'vulnerability':
        return sub.query.lower() in (r.id.lower() for r in res.vulnerabilities)
    else:
        return False


async def query_search(talkback_client: TalkbackClient,
                       sub_object: subscription.Subscription,
                       created_after: str,
                       created_before: str = None) -> List[resource.Resource]:
    """Query Talkback for resources matching the search query and other subscription requirements

    Args:
        talkback_client: TalkbackClient object
        sub_object: Subscription object
        created_after: Created after date in ISO format
        created_before: Created before date in ISO format
    Returns:
        List of Resource objects that match the subscription search query
    """

    search_results = await find_resources(
        talkback_client,
        sub_object.query,
        created_after,
        created_before)
    return [res for res in search_results if filter_resource(res, sub_object)]


async def get_all_results(talkback_client: TalkbackClient,
                          created_after: str,
                          created_before: str = None) -> List[resource.Resource]:
    """Get all resources from Talkback to filter further against subscriptions. This is necessary
    as the Talkback API does not support filtering by some required criteria, such as category,
    rank etc.

    Args:
        talkback_client: TalkbackClient object
        created_after: Created after date in ISO format
        created_before: Created before date in ISO format
    Returns:
        List of Resource objects
    """

    return await find_resources(talkback_client, 'title:*', created_after, created_before)


async def get_subscribed_content(talkback_client: TalkbackClient,
                                 subscriptions: List[subscription.Subscription],
                                 created_after: str,
                                 created_before) -> list[Tuple[resource.Resource, subscription.Subscription]]:
    """Get all resources from Talkback and filter against subscriptions

    Args:
        talkback_client: TalkbackClient object
        subscriptions: List of Subscription objects
        created_after: Created after date in ISO format
        created_before: Created before date in ISO format
    Returns:
        List containing tuples of Resource objects and the subscription they match 
    """

    filtered_results = []
    for sub in subscriptions:
        if sub.subscription_type == 'query':
            query_results = await query_search(talkback_client, sub, created_after, created_before)
            filtered_results.extend([(res, sub) for res in query_results])

    all_resources = await get_all_results(talkback_client, created_after, created_before)
    for sub in [s for s in subscriptions if s.subscription_type != 'query']:
        filtered_results.extend([(res, sub) for res in all_resources if filter_resource(res, sub)])

    return deduplicate_results(filtered_results)


async def validate_slack_user_id(user: str, slack_client: WebClient) -> str | None:
    """Validate the string for the user to send the message to is a user ID.
    First it checks if the string is an email address. If it is, it looks up
    the user and returns the ID. 
    
    If the string matches the format for a Slack user ID, it returns it.
    
    Otherwise, it returns None

    Args
        user: Either a Slack user ID or an email address
    Returns:
        User ID or None
    """

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, user):
        try:
            return slack_client.users_lookupByEmail(email=user).get('user').get('id')
        except SlackApiError as e:
            logger.error(f"Error looking up user: {e}")
            return None
    else:
        user_id_regex = r'^[UW][A-Z0-9]{8,11}$'
        if re.match(user_id_regex, user):
            return user
        else:
            return None


async def get_destinations(sub: subscription.Subscription,
                           slack_client: WebClient,
                           default_user: str,
                           default_channel: str) -> List[str]:
    """Get destinations for a given subscription. Checks if any 
    users or channels have been specified in the subscription. If not
    the default user and channel are used.

    Args:
        sub: Subscription object
        slack_client: Slack WebClient object
        default_user: Default user to post as
        default_channel: Default channel to post to
    Returns:
        List of users and/or channel IDs
    """

    destinations = []
    try:
        destinations.extend(sub.slack_destinations.channels)
    except AttributeError:
        pass
    try:
        for user in sub.slack_destinations.users:
            user_id = await validate_slack_user_id(user, slack_client)
            if user_id:
                destinations.append(user_id)
    except AttributeError:
        pass
    if not destinations:
        destinations.append(await validate_slack_user_id(default_user, slack_client))
        destinations.append(default_channel)
    return list(set(destinations))


async def send_slack_posts(resources: list[Tuple[resource.Resource, subscription.Subscription]],
                           slack_client: WebClient,
                           default_user: str,
                           default_channel: str) -> None:
    """Send Slack posts for resources that have matched subscriptions.
    Messages are sent to the channels and users specified in the subscriptions

    Args:
        resources: List of tuples containing Resource and Subscription objects
        slack_client: Slack WebClient object
        default_user: Default user to post as
        default_channel: Default channel to post to
    """

    for res, sub in resources:
        destinations = await get_destinations(sub, slack_client, default_user, default_channel)
        if not destinations:
            raise NoDestinationError(sub)

        for dest in destinations:
            try:
                slack_post_blocks = slack_builder.build_slack_post(res)
                post = slack_client.chat_postMessage(
                    channel=dest,
                    blocks=json.dumps(slack_post_blocks),
                    unfurl_links=False,
                    unfurl_media=False,
                    text=f'New resource: {res.title}',
                )
                post_timestamp = post.get('ts')
                thread_post = slack_builder.build_thread_message(res, sub)
                slack_client.chat_postMessage(
                    channel=dest,
                    thread_ts=post_timestamp,
                    blocks=json.dumps(thread_post),
                    unfurl_links=False,
                    unfurl_media=False,
                    text=f'Resource summary: {res.title}'
                )
                logger.info(f'Resource posted to {dest}: {res.title} - {post_timestamp}')
            except SlackApiError as e:
                logger.error(f'Error posting to Slack: {e}')
