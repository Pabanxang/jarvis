import requests
from core.logger import logger


def fetch_json(url, timeout=10):
    """
    Fetch JSON data from an API.
    Returns None if something goes wrong.
    """

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        logger.error(f"Network Error while fetching {url}: {e}")
        return None