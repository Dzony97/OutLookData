import os
import base64
import mimetypes
from pathlib import Path
import httpx
from dotenv import load_dotenv
from ms_graph import MS_GRAPH_BASE_URL

load_dotenv()
EMAIL = os.getenv('EMAIL')


def search_folders(headers: dict[str, str], folder_name: str) -> dict | None:
    endpoint = f'{MS_GRAPH_BASE_URL}/users/{EMAIL}/mailFolders'
    response = httpx.get(endpoint, headers=headers)
    response.raise_for_status()
    folders = response.json().get('value', [])
    for folder in folders:
        if folder['displayName'].lower() == folder_name.lower():
            return folder
    return None


def get_sub_folders(headers: dict[str, str], folder_id: int) -> dict | None:
    endpoint = f'{MS_GRAPH_BASE_URL}/users/{EMAIL}/mailFolders/{folder_id}/childFolders'
    response = httpx.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json().get('value', [])


def get_messages(headers: dict[str, str], folder_id: int | None, top=5, max_results=20, fields='*') -> list[...]:
    if folder_id is None:
        endpoint = f'{MS_GRAPH_BASE_URL}/users/{EMAIL}/messages'
    else:
        endpoint = f'{MS_GRAPH_BASE_URL}/users/{EMAIL}/mailFolders/{str(folder_id)}/messages'

    params = {
        '$top': min(top, max_results),
        '$select': fields,
        '$orderby': 'receivedDateTime desc'
    }

    messages = []
    next_link = endpoint

    while next_link and len(messages) < max_results:
        response = httpx.get(next_link, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f'Failed to retrieve emails: {response.json()}')

        json_response = response.json()
        messages.extend(json_response.get('value', []))
        next_link = json_response.get('nextLink', None)
        params = None

        if next_link and len(messages) + top > max_results:
            params = {
                '$top': max_results - len(messages)
            }

    return messages[:max_results]


def search_messages(headers: dict[str, str], search_query: str, folder_id=None, fields='*', top=5,
                    max_results=20) -> list[...]:
    if folder_id is None:
        endpoint = f'{MS_GRAPH_BASE_URL}/users/{EMAIL}/messages'
    else:
        endpoint = f'{MS_GRAPH_BASE_URL}/users/{EMAIL}/mailFolders/{str(folder_id)}/messages'

    params = {
        '$top': min(top, max_results),
        '$select': fields,
        '$search': f'{search_query}',
    }

    messages = []
    next_link = endpoint

    while next_link and len(messages) < max_results:
        response = httpx.get(next_link, headers=headers, params=params)
        response.raise_for_status()

        if response.status_code != 200:
            raise Exception(f'Failed to retrieve emails: {response.json()}')

        json_response = response.json()
        messages.extend(json_response.get('value', []))
        next_link = json_response.get('nextLink', None)
        params = None

        if next_link and len(messages) + top > max_results:
            params = {
                '$top': max_results - len(messages)
            }

    return messages[:max_results]
