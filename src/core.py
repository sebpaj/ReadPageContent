import os
import webbrowser

from src.utils import (
    get_html_content,
    handle_count_top_words_occurence,
)


def open_page_from_url(url: str) -> None:
    webbrowser.open(url)


def get_most_frequent_words_from_url(url: str) -> list[dict[str, int]]:
    html_content = get_html_content(url)
    if not html_content:
        raise ValueError("Could not get html data")

    top_words_occurence = handle_count_top_words_occurence(html_content)

    return top_words_occurence


def generate_and_save_results(top_words_occurence: list[dict[str, int]]) -> None:
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Top most frequent words</title>
    </head>
    <body>
        <h1>Top most frequent words</h1>
    """

    for item in top_words_occurence:
        list_items = "".join(f"<li>{key}: {value}</li>" for key, value in item.items())
        html_content += f"<ul>{list_items}</ul>"

    html_content += """
    </body>
    </html>
    """

    with open("../result.html", "w") as html_file:
        html_file.write(html_content)

    with open("../result.txt", "w") as file:
        file.write(str(top_words_occurence))


def open_results() -> None:
    filepath = os.path.abspath("../result.html")

    webbrowser.open("file://" + filepath)
