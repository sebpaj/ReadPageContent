from typing import Optional
import re
import requests


def get_html_content(url: str) -> Optional[str]:
    response = requests.get(url)
    if not response.status_code == 200:
        return None
    return response.text


def get_clean_html_content(html_content: str) -> str:
    # Remove the content of script tags
    script_content = re.compile(r"<script.*?>.*?</script>", re.DOTALL)
    html_content = re.sub(script_content, "", html_content)

    # Remove the content of style tags
    style_content = re.compile(r"<style.*?>.*?</style>", re.DOTALL)
    html_content = re.sub(style_content, "", html_content)

    # Remove HTML comments
    html_comments = re.compile(r"<!--.*?-->", re.DOTALL)
    html_content = re.sub(html_comments, "", html_content)

    # Remove HTML tags
    html_tags = re.compile(r"<[^>]+>")
    html_content = re.sub(html_tags, "", html_content)

    # Remove HTML entities
    html_entities = re.compile(r"&[^;]+;")
    html_content = re.sub(html_entities, "", html_content)

    # Remove special characters and punctuation
    special_chars_punctuation = re.compile(r"[^\w\s]")
    html_content = re.sub(special_chars_punctuation, "", html_content)

    return html_content


def get_words_from_html(text: str) -> list[str]:
    return text.lower().strip().split(" ")


def clean_words(words: list[str]) -> list[str]:
    return [s.strip() for s in words if s.strip()]


def count_word_occurences(
    words: list[str], sort_words: bool = False, reverse: bool = False
) -> dict[str, int]:
    word_occurences = {}

    for word in words:
        word_occurences[word] = word_occurences.get(word, 0) + 1

    if sort_words:
        sorted_word_occurences = dict(
            sorted(word_occurences.items(), key=lambda item: item[1], reverse=reverse)
        )
        return sorted_word_occurences

    return word_occurences


def get_top_word_occurences(
    words_with_occurence: dict[str, int]
) -> list[dict[str, int]]:
    rank = 0
    prev_occurence_value = None
    top_10_occurences = []
    rank_counts = 1

    for word, occurence in words_with_occurence.items():
        if occurence != prev_occurence_value:
            rank += rank_counts
            prev_occurence_value = occurence
            rank_counts = 1
        else:
            rank_counts += 1

        if rank > 10:
            break

        top_10_occurences.append({word: occurence})

    return top_10_occurences


def handle_count_top_words_occurence(html_content: str) -> list[dict[str, int]]:
    clean_html_content = get_clean_html_content(html_content)

    words_from_html = get_words_from_html(clean_html_content)

    cleaned_words = clean_words(words_from_html)

    word_occurences = count_word_occurences(cleaned_words, True, True)

    top_word_occurences = get_top_word_occurences(word_occurences)

    return top_word_occurences
