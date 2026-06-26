from collections import deque
from urllib.parse import urljoin, urlparse
import json

from bs4 import BeautifulSoup

from utils import download_page
from scraper import scrape_website


# Crawl these pages first
PRIORITY_KEYWORDS = [
    "about",
    "service",
    "solution",
    "ai",
    "product",
    "industry",
    "case",
    "portfolio",
    "client",
    "career",
    "contact",
    "team",
]

# Skip these pages
SKIP_KEYWORDS = [
    "privacy",
    "terms",
    "cookie",
    "login",
    "signup",
    "register",
    "feed",
    "rss",
    "wp-admin",
]


def normalize_url(url):
    return url.rstrip("/")


def get_priority(url):
    url = url.lower()

    for index, keyword in enumerate(PRIORITY_KEYWORDS):
        if keyword in url:
            return index

    if "blog" in url:
        return 100

    return 50


def extract_links(url):
    """
    Extract all valid internal links from one page.
    """

    response = download_page(url)

    soup = BeautifulSoup(response.text, "html.parser")

    base_domain = urlparse(url).netloc

    links = []

    for tag in soup.find_all("a", href=True):

        href = tag["href"]

        if not href:
            continue

        if href.startswith("#"):
            continue

        if href.startswith("mailto:"):
            continue

        if href.startswith("tel:"):
            continue

        if href.startswith("javascript"):
            continue

        full_url = normalize_url(
            urljoin(url, href)
        )

        parsed = urlparse(full_url)

        if parsed.netloc != base_domain:
            continue

        if any(
            word in full_url.lower()
            for word in SKIP_KEYWORDS
        ):
            continue

        links.append(full_url)

    links = list(set(links))

    links.sort(key=get_priority)

    return links


def crawl_website(start_url, max_pages=50):
    """
    Crawl a website using Breadth-First Search.

    Returns:
        [
            {
                "url": "...",
                "text": "..."
            },
            ...
        ]
    """

    start_url = normalize_url(start_url)

    visited = set()

    queue = deque([start_url])

    pages = []

    while queue and len(visited) < max_pages:

        current_url = queue.popleft()

        if current_url in visited:
            continue

        visited.add(current_url)

        print(f"Scraping ({len(visited)}/{max_pages}) : {current_url}")

        try:

            text = scrape_website(current_url)

            pages.append({
                "url": current_url,
                "text": text
            })

            links = extract_links(current_url)

            for link in links:

                if link not in visited and link not in queue:
                    queue.append(link)

        except Exception as e:

            print(f"Skipped : {current_url}")

            print(e)

    total_characters = sum(
        len(page["text"])
        for page in pages
    )

    print("\n" + "=" * 80)
    print(f"Pages Crawled : {len(pages)}")
    print(f"Characters    : {total_characters:,}")
    print("=" * 80)

    return pages


if __name__ == "__main__":

    website = "https://www.e2msolutions.com"

    pages = crawl_website(
        website,
        max_pages=50
    )

    with open(
        "website_content.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            pages,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nSaved to website_content.json")

    if pages:

        print("\nPreview\n")
        print("=" * 80)

        print("URL:")
        print(pages[0]["url"])

        print("\nFirst 1500 characters:\n")

        print(pages[0]["text"][:1500])