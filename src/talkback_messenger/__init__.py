import argparse
import asyncio
import os
from datetime import datetime, timedelta
from typing import List, Tuple

from loguru import logger
from slack_sdk import WebClient

from talkback_messenger import talkback_bot_core
from talkback_messenger.clients.talkback_client import TalkbackClient
from talkback_messenger.models import subscription, resource
from talkback_messenger.utils import init_logger
from talkback_messenger.utils import load_config


async def search_subscribed_content(talkback_client: TalkbackClient,
                                    subscription_list: List[subscription.Subscription],
                                    start_time: str,
                                    end_time: str) -> list[Tuple[resource.Resource, subscription.Subscription]]:
    """Search for content set out in the loaded subscriptions

    Args:
        talkback_client: TalkbackClient object
        subscription_list: List of Subscription objects
        start_time: Start time for search
        end_time: End time for search
    Returns:
        List of Resource objects
    """

    return await talkback_bot_core.get_subscribed_content(
        talkback_client,
        subscription_list,
        start_time,
        end_time)


async def post_to_slack(resources: list[Tuple[resource.Resource, subscription.Subscription]],
                        slack_client: WebClient,
                        default_user: str,
                        default_channel: str) -> None:
    """Post resources to Slack

    Args:
        resources: List of resources
        slack_client: Slack WebClient object
        default_user: Default user to post as
        default_channel: Default channel to post to
    """
    await talkback_bot_core.send_slack_posts(resources, slack_client, default_user, default_channel)


async def init_slack_client() -> WebClient | None:
    """Initialise the Slack WebClient object and test the connection

    Returns:
        WebClient object
    """

    slack_client = WebClient(token=os.getenv('SLACK_API_TOKEN'))
    response = slack_client.api_test()
    if response.get('ok'):
        logger.info('Slack API connection successful')
        return slack_client
    else:
        raise ConnectionError('Slack API connection failed')


async def validate_environment_variables():
    """Validate that the required environment variables are set
        and raise an error if not
    """

    if not os.getenv('TALKBACK_API_TOKEN'):
        raise ValueError('TALKBACK_API_TOKEN environment variable not set')
    if not os.getenv('SLACK_API_TOKEN'):
        raise ValueError('SLACK_API_TOKEN environment variable not set')


# pylint: disable=missing-function-docstring, too-many-locals
async def main_coroutine():
    try:
        parser = argparse.ArgumentParser(description='Talkback Slack Bot')
        parser.add_argument(
            '--config',
            type=str,
            dest='config',
            help='Path to the configuration file. '
                 'Do not use if you are running in a container and have mounted the config file')
        parser.add_argument(
            '--timeframe',
            choices=range(1, 25),
            type=int,
            dest='timeframe',
            help='How many hours back to search (1-24)',
            required=True)
        parser.add_argument(
            '--debug', '-d',
            dest='debug',
            action='store_true',
            help='Turn on debug level logging')
        args = parser.parse_args()
        config_path = args.config
        timeframe = args.timeframe
        debug = args.debug

        await validate_environment_variables()
        await init_logger(debug)

        if timeframe != 24:
            end_time = datetime.now().replace(minute=0, second=0, microsecond=0)
            start_time = end_time - timedelta(hours=timeframe)

            created_before = end_time.isoformat()
            created_after = start_time.isoformat()
        else:
            start_of_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start_of_previous_day = start_of_today - timedelta(days=1)
            end_of_previous_day = start_of_today - timedelta(microseconds=1)

            created_after = start_of_previous_day.isoformat()
            created_before = end_of_previous_day.isoformat()

        talkback_client = TalkbackClient('https://talkback.sh/api/v1/', os.getenv('TALKBACK_API_TOKEN'))
        await talkback_client.refresh_token()
        slack_client = await init_slack_client()

        logger.info('Importing subscriptions')
        if not config_path:
            logger.info('No config path provided. Attempting to load from /etc/talkback-messenger/talkback.conf')
            config_path = '/etc/talkback-messenger/talkback.conf'
        app_config = await talkback_bot_core.load_app_config(config_path)
        logger.info(f'{len(app_config.subscriptions)} subscriptions imported')
        for sub in app_config.subscriptions:
            logger.debug(str(sub))
        logger.info('Searching for subscribed content')
        logger.info(f'Searching for resources created between {created_after} and {created_before}')
        results = await search_subscribed_content(
            talkback_client=talkback_client,
            subscription_list=app_config.subscriptions,
            start_time=created_after,
            end_time=created_before)
        if results:
            logger.success(f'{len(results)} resources found')
            logger.info('Posting to Slack')
            await post_to_slack(results, slack_client, app_config.default_user, app_config.default_channel)
        else:
            logger.info('No resources found')
        logger.success('Finished Talkback Slack Bot')
    except Exception as e:
        logger.exception(e)


# pylint: disable=missing-function-docstring
def main():
    asyncio.run(main_coroutine())


if __name__ == '__main__':
    main()
