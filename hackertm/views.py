import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from django.http import HttpRequest, HttpResponse
from .settings import ORIGINAL_URL
from .utils import (
    add_trademark_to_6_letter_words,
    make_attribute_url_absolute,
    make_attribute_url_relative,
)


def index(request: HttpRequest) -> HttpResponse:
    try:
        response = requests.get(
            ORIGINAL_URL + request.path, params=request.GET
        )
        html = response.text
    except RequestException as e:
        return HttpResponse(f"Error fetching content: {str(e)}", status=500)

    soup = BeautifulSoup(html, 'html.parser')

    # Convert all relative urls for css, js, and images
    # to link the original site
    for node in soup.find_all('link', rel='stylesheet'):
        make_attribute_url_absolute(node, 'href', ORIGINAL_URL)

    for node in soup.find_all('img'):
        make_attribute_url_absolute(node, 'src', ORIGINAL_URL)

    for node in soup.find_all('script'):
        make_attribute_url_absolute(node, 'src', ORIGINAL_URL)

    # Change all links to the original site to link our proxy
    for node in soup.find_all('a'):
        make_attribute_url_relative(node, 'href', ORIGINAL_URL)

    # Add trademark symbols to the text nodes
    # text = add_trademark_to_6_letter_words(text)
    for text_node in soup.find_all(text=True):
        text_node.string.replace_with(
            add_trademark_to_6_letter_words(text_node.string)
        )

    return HttpResponse(str(soup))
