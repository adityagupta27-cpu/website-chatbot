from bs4 import BeautifulSoup

from utils import download_page


def scrape_website(url):
    """
    Downloads one webpage and extracts visible text.
    """

    response = download_page(url)

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text