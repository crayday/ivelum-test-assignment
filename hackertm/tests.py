from bs4 import BeautifulSoup
from django.test import TestCase
from .utils import (
    add_trademark_to_6_letter_words,
    make_attribute_url_absolute,
    make_attribute_url_relative,
)


class TestHackerTM(TestCase):
    def test_add_trademark_to_6_letter_words(self) -> None:
        text = """
            The visual description of the colliding files, at
            http://shattered.io/static/pdf_format.png, is not very helpful
            in understanding how they produced the PDFs, so I took apart
            the PDFs and worked it out.

            Basically, each PDF contains a single large (421,385-byte) JPG
            image, followed by a few PDF commands to display the JPG. The
            collision lives entirely in the JPG data - the PDF format is
            merely incidental here. Extracting out the two images shows two
            JPG files with different contents (but different SHA-1 hashes
            since the necessary prefix is missing). Each PDF consists of a
            common prefix (which contains the PDF header, JPG stream
            descriptor and some JPG headers), and a common suffix (containing
            image data and PDF display commands).
        """

        expected_trademarked_text = """
            The visual™ description of the colliding files, at
            http://shattered.io/static/pdf_format.png, is not very helpful
            in understanding how they produced the PDFs, so I took apart
            the PDFs and worked™ it out.

            Basically, each PDF contains a single™ large (421,385-byte) JPG
            image, followed by a few PDF commands to display the JPG. The
            collision lives entirely in the JPG data - the PDF format™ is
            merely™ incidental here. Extracting out the two images™ shows two
            JPG files with different contents (but different SHA-1 hashes™
            since the necessary prefix™ is missing). Each PDF consists of a
            common™ prefix™ (which contains the PDF header™, JPG stream™
            descriptor and some JPG headers), and a common™ suffix™ (containing
            image data and PDF display commands).
        """

        trademarked_text = add_trademark_to_6_letter_words(text)
        self.assertEqual(trademarked_text, expected_trademarked_text)

    def test_make_attribute_url_relative(self) -> None:
        base_url = "http://foo.bar"

        # Test with an absolute URL
        html = "<a href='http://foo.bar/buz'>"
        soup = BeautifulSoup(html, "html.parser")
        node = soup.find("a")
        make_attribute_url_relative(node, "href", base_url)
        self.assertEqual(node["href"], "/buz")

        # Test with an absolute URL pointing to the other site
        html = "<a href='http://another.bar/buz'>"
        soup = BeautifulSoup(html, "html.parser")
        node = soup.find("a")
        make_attribute_url_relative(node, "href", base_url)
        self.assertEqual(node["href"], "http://another.bar/buz")

        # Test with a relative URL
        html = "<a href='/buz'>"
        soup = BeautifulSoup(html, "html.parser")
        node = soup.find("a")
        make_attribute_url_relative(node, "href", base_url)
        self.assertEqual(node["href"], "/buz")

        # Test with no href attribute
        html = "<a>"
        soup = BeautifulSoup(html, "html.parser")
        node = soup.find("a")
        make_attribute_url_relative(node, "href", base_url)
        self.assertFalse(node.has_attr("href"))

    def test_make_attribute_url_absolute(self) -> None:
        base_url = "http://foo.bar"

        # Test with a relative URL starting with /
        html = "<img src='/images/img.jpg'>"
        soup = BeautifulSoup(html, "html.parser")
        node = soup.find("img")
        make_attribute_url_absolute(node, "src", base_url)
        self.assertEqual(node["src"], "http://foo.bar/images/img.jpg")

        # Test with a relative URL not starting with /
        html = "<img src='images/img.jpg'>"
        soup = BeautifulSoup(html, "html.parser")
        node = soup.find("img")
        make_attribute_url_absolute(node, "src", base_url)
        self.assertEqual(node["src"], "http://foo.bar/images/img.jpg")

        # Test with an absolute URL to the other site
        html = "<img src='http://other.bar/images/img.jpg'>"
        soup = BeautifulSoup(html, "html.parser")
        node = soup.find("img")
        make_attribute_url_absolute(node, "src", base_url)
        self.assertEqual(node["src"], "http://other.bar/images/img.jpg")

        # Test with no src attribute
        html = "<img>"
        soup = BeautifulSoup(html, "html.parser")
        node = soup.find("img")
        make_attribute_url_absolute(node, "src", base_url)
        self.assertFalse(node.has_attr("src"))
