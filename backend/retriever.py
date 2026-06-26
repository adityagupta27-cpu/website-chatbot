import re
from collections import Counter

# Common English words that don't help retrieval
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "to", "of", "for", "in", "on", "at", "by",
    "what", "which", "who", "where", "when", "why",
    "how", "does", "do", "did", "can", "could",
    "should", "would", "will", "about", "tell",
    "me", "their", "they", "this", "that",
    "company", "please", "give", "show"
}

# URLs containing these keywords receive a ranking boost
URL_BOOST = {
    "about": 6,
    "service": 12,
    "services": 12,
    "solution": 10,
    "solutions": 10,
    "ai": 15,
    "llm": 15,
    "automation": 12,
    "machine-learning": 12,
    "career": 4,
    "contact": 3,
    "product": 8,
    "case": 6,
    "industry": 5,
    "portfolio": 5,
}


def tokenize(text):
    """
    Convert text into clean searchable words.
    """

    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return [
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 2
    ]


def keyword_score(question_words, page_words):
    """
    Score based on keyword frequency.
    """

    page_counter = Counter(page_words)

    score = 0

    for word in question_words:

        if word in page_counter:

            # Give higher score for repeated occurrences
            score += page_counter[word]

    return score


def url_score(url, question_words):
    """
    Give extra score if the URL itself matches.
    """

    score = 0

    url = url.lower()

    for word in question_words:

        if word in url:
            score += 8

    for keyword, boost in URL_BOOST.items():

        if keyword in url:
            score += boost

    return score


def retrieve(question, pages, top_k=5):
    """
    Retrieve the most relevant pages.

    Returns:
        List of page dictionaries.
    """

    question_words = tokenize(question)

    ranked_pages = []

    for page in pages:

        page_words = tokenize(page["text"])

        score = 0

        score += keyword_score(
            question_words,
            page_words
        )

        score += url_score(
            page["url"],
            question_words
        )

        ranked_pages.append(
            {
                "score": score,
                "url": page["url"],
                "text": page["text"]
            }
        )

    ranked_pages.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    relevant_pages = []

    for page in ranked_pages:

        if page["score"] <= 0:
            continue

        relevant_pages.append(
            {
                "url": page["url"],
                "text": page["text"]
            }
        )

        if len(relevant_pages) == top_k:
            break

    return relevant_pages


# -------------------------
# Local Testing
# -------------------------

if __name__ == "__main__":

    import json

    with open(
        "website_content.json",
        "r",
        encoding="utf-8"
    ) as f:

        pages = json.load(f)

    question = "What AI services do they provide?"

    results = retrieve(
        question,
        pages,
        top_k=5
    )

    print("\nTop Retrieved Pages\n")

    for i, page in enumerate(results, start=1):

        print("=" * 70)

        print(f"Rank {i}")

        print(page["url"])

        print(page["text"][:300])

        print()