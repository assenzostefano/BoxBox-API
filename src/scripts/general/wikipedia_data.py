import os
from urllib.parse import urlsplit

import requests


def wikipedia_data(url_wikipedia):
    try:
        # Splits the link and takes only the final part of the Wikipedia link
        parsed_link = urlsplit(url_wikipedia)
        path = parsed_link.path
        filename = os.path.basename(path)
        page_title = os.path.splitext(filename)[0]

        # Wikipedia API Biography
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
        url_wikipedia = url + page_title
        response = requests.get(url_wikipedia).json()
    except:
        response = ""

    return response