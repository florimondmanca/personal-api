"""Blog utilities."""

from bs4 import BeautifulSoup
from markdown import markdown


def markdown_unformatted(markup: str, sep="") -> str:
    """Remove formatting from a markdown text."""
    html = markdown(markup)
    soup = BeautifulSoup(html, "html.parser")
    text = sep.join(soup.findAll(text=True))
    return text
