import requests


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
        print(f"Network Error: {e}")

        return None