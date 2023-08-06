from __future__ import annotations
import socket
from collections import defaultdict
from typing import Any

import requests


def get_local_ip() -> str:
    """Get local IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip


def get_public_ip() -> str:
    """Get public IP address.

    Return the public IP address if it is available, otherwise return 127.0.0.1.
    """
    try:
        return requests.get('https://api.ipify.org').text
    except requests.exceptions.RequestException:
        return '127.0.0.1'


def get_public_ip_json() -> dict[str, Any]:
    """Get public IP address as JSON."""
    try:
        return requests.get('https://ipinfo.io/json').json()
    except requests.exceptions.RequestException:
        return defaultdict(str, {'ip': '127.0.0.1'})


def get_ip_info(ip: str) -> dict[str, Any]:
    """Retrieves the information about the IP address."""
    url = f'https://freegeoip.app/json/{ip}'
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }
    try:
        return requests.get(url, headers=headers).json()
    except requests.exceptions.RequestException:
        return defaultdict(str, {'ip': '127.0.0.1'})
