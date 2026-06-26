import re


def retrieve(question, pages, top_k=5):
    """
    Return the most relevant pages using keyword matching.
    """

    question_words = set(
        re.findall(r"\w+", question.lower())
    )

    scored_pages = []

    for page in pages:

        page_words = set(
            re.findall(r"\w+", page["text"].lower())
        )

        score = len(
            question_words & page_words
        )

        scored_pages.append(
            (
                score,
                page
            )
        )

    scored_pages.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        page
        for score, page in scored_pages[:top_k]
        if score > 0
    ]
