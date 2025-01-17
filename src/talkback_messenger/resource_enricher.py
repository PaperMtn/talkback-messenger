"""Module to enrich Talkback resources by scraping the webpage using BeautifulSoup

This module contains functions to scrape the Talkback resource webpage and extract
information that is not included in the Talkback API response.
This includes:
- Synopsis
- Summary
- Topics
- Vulnerabilities

Typical usage example:
    information = populate_information('https://talkback.sh/resource/abc-123/')
"""

from typing import Dict, List, Any

import requests
from bs4 import BeautifulSoup


def _get_synopsis(html_output: BeautifulSoup) -> Dict[str, str]:
    spans = html_output.find_all('span')
    for s in spans:
        if s.get_text() == 'Synopsis':
            siblings = s.fetchNextSiblings()
            paragraphs = [element.get_text() for element in siblings if element.name == 'p']
            information_dict = {
                'synopsis': paragraphs[0] if paragraphs else None,
                'summary': paragraphs[1:] if len(paragraphs) > 1 else []
            }

            return information_dict
    return {}


def _get_topics(html_content):
    topics = []
    topic_elements = html_content.select('.card:has(h6.card-header:-soup-contains("Topics")) .list-group-item')
    for topic in topic_elements:
        title = topic.select_one('.text-primary').text.strip()
        vendor = topic.select_one('.text-secondary').text.strip() if topic.select_one('.text-secondary') else None
        topic_type = topic.select_one('.text-body-tertiary').text.strip().split('\n')[0] if topic.select_one(
            '.text-body-tertiary') else None
        topics.append({'title': title, 'vendor': vendor, 'type': topic_type})

    return topics


def _get_vulnerabilities(html_output: BeautifulSoup) -> List[Dict[str, str]]:
    vulns = []
    vuln_elements = html_output.select('.card:has(h6.card-header:-soup-contains("Vulns")) .list-group-item')
    for vuln in vuln_elements:
        name = vuln.select_one('.text-primary').text.strip()
        cvss = vuln.select_one('.text-secondary').text.strip() if vuln.select_one('.text-secondary') else None
        cwes = [cwe.strip() for cwe in vuln.select('.text-truncate span') if cwe.strip()]
        url = f'https://talkback.sh/vulnerability/{name}/'
        vulns.append({'name': name, 'cvss': cvss, 'cwes': cwes, 'url': url})

    return vulns


def populate_information(url: str) -> dict[Any, Any]:
    """Populate information from a Talkback resource URL by scraping the webpage

    Args:
        url: URL of the Talkback resource
    Returns:
        Dictionary containing the synopsis, summary, topics and vulnerabilities of the resource
        Example:
        {
            'synopsis': 'This is a synopsis',
            'summary': ['This is a summary'],
            'topics': [{'title': 'Topic', 'vendor': 'Vendor', 'type': 'Type'}],
            'vulnerabilities': [
                {
                    'name': 'Vulnerability',
                    'cvss': 'CVSS',
                    'cwes': ['CWE1', 'CWE2'],
                    'url': 'https://talkback.sh/vulnerability/Vulnerability/'
                }
            ]
        }
    """

    response = requests.get(url, timeout=60)
    html_output = BeautifulSoup(response.text, 'html.parser')

    output_dict = {}
    summary_information = _get_synopsis(html_output)
    output_dict['synopsis'] = summary_information.get('synopsis', None)
    output_dict['summary'] = summary_information.get('summary', [])
    output_dict['topics'] = _get_topics(html_output)
    output_dict['vulnerabilities'] = _get_vulnerabilities(html_output)

    return output_dict
