"""Talkback API client

This module provides a client for the Talkback API. Uses the gql library to interact with the API.

Typical usage example:
    from talkback_messenger.clients import talkback_client
    client = talkback_client.TalkbackClient(api_url, token)

    query_results = await client.search_resources(search, created_after)
"""

from datetime import datetime
from typing import Any, Dict, List

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


class TalkbackClient:
    """ Client for the Talkback API

    Attributes:
        api_url: URL of the Talkback API
        token: JWT token for the Talkback API
    """

    def __init__(self, api_url, token):
        self.api_url = api_url
        self.token = token
        self.transport = AIOHTTPTransport(
            url=self.api_url,
            headers={'Authorization': f'JWT {self.token}'},
            timeout=60,
        )
        self.client = Client(
            transport=self.transport,
            execute_timeout=60,
            fetch_schema_from_transport=False)

    async def _execute_query(self, query: str, variables: Dict[Any, Any] = None) -> Dict[Any, Any]:
        async with self.client as session:
            return await session.execute(gql(query), variable_values=variables)

    async def validate_token(self) -> Dict[Any, Any]:
        """ Validate the Talkback API token"""

        query = """
            mutation VerifyToken($token: String!) {
                verifyToken(token: $token) {
                    payload
                }
            }
        """
        variables = {'token': self.token}
        response = await self._execute_query(query, variables)
        return response

    async def refresh_token(self) -> Dict[Any, Any]:
        """ Refresh the Talkback API token"""

        query = """
            mutation RefreshToken($token: String!) {
              refreshToken(token: $token) {
                token
              }
            }
        """
        variables = {'token': self.token}
        response = await self._execute_query(query, variables)
        self.token = response['refreshToken']['token']
        return response

    async def search_resources(self,
                               search: str,
                               created_after: str,
                               created_before: str = datetime.now().isoformat(),
                               first: int = 100) -> List[Dict[Any, Any]]:
        """Search for resources from Talkback
        Args:
            search: Search query
            created_after: Created after date
            created_before: Created before date
            first: Number of resources to fetch
        Returns:
            List of resources
        """

        query = """
            query GetResources($search: String!, $first: Int, $after: String, $createdAfter: DateTime, $createdBefore: DateTime) {
              resources(q: $search, first: $first, after: $after, createdDateAfter: $createdAfter, createdDateBefore: $createdBefore) {
                edges {
                  node {
                    id
                    url
                    type
                    createdDate
                    title
                    domain {
                      name
                    }
                    curators {
                      name
                      url
                    }
                    categories {
                      fullname
                    }
                    rank
                    tier
                    readtime
                  }
                }
                pageInfo {
                  hasNextPage
                  endCursor
                }
              }
            }
        """
        variables = {
            'search': search,
            'first': first,
            'after': None,
            'createdAfter': created_after,
            'createdBefore': created_before
        }
        all_resources = []

        while True:
            response = await self._execute_query(query, variables)
            edges = response['resources']['edges']
            page_info = response['resources']['pageInfo']
            for edge in edges:
                all_resources.append(edge['node'])

            if not page_info['hasNextPage']:
                break

            variables['after'] = page_info['endCursor']
        return all_resources
