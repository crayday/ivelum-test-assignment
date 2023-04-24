import re
from bs4 import Tag


def add_trademark_to_6_letter_words(text: str) -> str:
    """
    Add ™ symbol to all 6-letter words but look behind for a "." or "/"
    symbol to not to not match urls in the text.
    """
    return re.sub(r'(?<![./])\b(\w{6})\b', r'\g<1>™', text)


def make_attribute_url_absolute(
    node: Tag, attr_name: str, base_url: str
) -> None:
    """
    Convert relative URL in the given attribute to an absolute
    using the provided base URL.
    """
    if not node.has_attr(attr_name) or re.match(r'https?://', node[attr_name]):
        return
    if node[attr_name].startswith('/'):
        node[attr_name] = base_url + node[attr_name]
    else:
        node[attr_name] = base_url + '/' + node[attr_name]


def make_attribute_url_relative(
    node: Tag, attr_name: str, base_url: str
) -> None:
    """
    Convert an absolute URL pointing at the base URL to relative
    """
    if node.has_attr(attr_name) and node[attr_name].startswith(base_url):
        node[attr_name] = node[attr_name][len(base_url):]
