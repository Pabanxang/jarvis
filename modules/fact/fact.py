from core.internet import fetch_json


URL = "https://uselessfacts.jsph.pl/api/v2/facts/random"


def get_fact():

    data = fetch_json(URL)

    if data:

        return data["text"]

    return "Couldn't fetch today's fact."