from collections import deque
from urllib.parse import urljoin, urlparse
import json
import os

from bs4 import BeautifulSoup

from utils import download_page
from scraper import scrape_website

from config import (
    MAX_PAGES,
    CACHE_FILE
)


# Pages we want to crawl first
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


# Pages we don't need
SKIP_KEYWORDS = [
    "privacy",
    "terms",
    "cookie",
    "login",
    "signup",
    "register",
    "rss",
    "feed",
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

    response = download_page(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

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


def crawl_website(
    start_url,
    max_pages=MAX_PAGES
):

    print("\nStarting crawl...\n")

    start_url = normalize_url(start_url)

    visited = set()

    queue = deque([start_url])

    pages = []
    while queue and len(visited) < max_pages:

        current_url = queue.popleft()

        if current_url in visited:
            continue

        visited.add(current_url)

        print(
            f"[{len(visited)}/{max_pages}] Crawling: {current_url}"
        )

        try:

            page_text = scrape_website(current_url)

            if page_text.strip():

                pages.append(
                    {
                        "url": current_url,
                        "text": page_text
                    }
                )

            links = extract_links(current_url)

            for link in links:

                if (
                    link not in visited
                    and link not in queue
                ):
                    queue.append(link)

        except Exception as e:

            print(f"Skipped: {current_url}")

            print(e)

    total_characters = sum(
        len(page["text"])
        for page in pages
    )

    print("\n" + "=" * 80)

    print(f"Pages Crawled : {len(pages)}")

    print(
        f"Characters    : {total_characters:,}"
    )

    print("=" * 80)

    return pages


def save_cache(pages):

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            pages,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nKnowledge base saved to {CACHE_FILE}"
    )


def load_cache():

    if not os.path.exists(CACHE_FILE):

        return None

    with open(
        CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        pages = json.load(file)

    print(
        f"Loaded {len(pages)} pages from cache."
    )

    return pages
if __name__ == "__main__":

    WEBSITE = "https://www.e2msolutions.com"

    pages = crawl_website(
        WEBSITE,
        max_pages=MAX_PAGES
    )

    save_cache(pages)

    print("\n" + "=" * 80)
    print("CRAWLING COMPLETED")
    print("=" * 80)
    print(f"Pages Saved : {len(pages)}")
    print(f"Cache File  : {CACHE_FILE}")

    if pages:

        print("\nFirst Page Preview")
        print("-" * 80)

        print("URL:")
        print(pages[0]["url"])

        print("\nPreview:\n")

        print(
            pages[0]["text"][:1500]
        )

        print("\n" + "-" * 80)