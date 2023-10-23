from unittest.mock import patch
import pytest
from src.utils import (
    clean_words,
    count_word_occurences,
    get_clean_html_content,
    get_html_content,
    get_top_word_occurences,
    get_words_from_html,
    handle_count_top_words_occurence,
)


@pytest.fixture()
def mock_funcs():
    with patch("src.utils.get_clean_html_content") as mock_clean, patch(
        "src.utils.get_words_from_html"
    ) as mock_words, patch("src.utils.clean_words") as mock_cleaned_words, patch(
        "src.utils.count_word_occurences"
    ) as mock_count, patch(
        "src.utils.get_top_word_occurences"
    ) as mock_top:
        yield mock_clean, mock_words, mock_cleaned_words, mock_count, mock_top


@patch("requests.get")
def test_get_html_content(mock_get):
    # Given
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "Success"

    # When
    result = get_html_content("http://example.com")

    # Then
    assert result == "Success"


@patch("requests.get")
def test_get_html_content_failure(mock_get):
    # Given
    mock_get.return_value.status_code = 404

    # When
    result = get_html_content("http://example.com")

    # Then
    assert result is None


def test_remove_script_tags():
    # Given
    html = "<script type='text/javascript'>var a = 'Hello World';</script>"

    # When
    clean_html = get_clean_html_content(html)

    # Then
    assert clean_html == ""


def test_remove_style_tags():
    # Given
    html = "<style>.text { color: red; }</style>"

    # When
    clean_html = get_clean_html_content(html)

    # Then
    assert clean_html == ""


def test_remove_html_comments():
    # Given
    html = "<!-- This is a comment -->"

    # When
    clean_html = get_clean_html_content(html)

    # Then
    assert clean_html == ""


def test_remove_html_tags():
    # Given
    html = "<p>This is a paragraph.</p>"

    # When
    clean_html = get_clean_html_content(html)

    # Then
    assert clean_html == "This is a paragraph"


def test_remove_html_entities():
    # Given
    html = "&lt;&gt;This is a test.&lt;/&gt;"

    # When
    clean_html = get_clean_html_content(html)

    # Then
    assert clean_html == "This is a test"


def test_remove_special_chars_and_punctuation():
    # Given
    html = "Special!@#$%^&*()+{}: characters."

    # When
    clean_html = get_clean_html_content(html)

    # Then
    assert clean_html == "Special characters"


def test_get_words_from_html():
    # Given
    text = "  Hello, World! This is a simple test.  "
    expected_result = ["hello,", "world!", "this", "is", "a", "simple", "test."]

    # When
    result = get_words_from_html(text)

    # Then
    assert result == expected_result


def test_clean_words():
    # Given
    words_list = ["  hello  ", "world", "", " ", "python  ", "\tjava\r", "\n"]
    expected_result = ["hello", "world", "python", "java"]

    # Process the list of words
    result = clean_words(words_list)

    # Then
    assert result == expected_result


def test_counting_occurences():
    # Given
    words = ["hello", "world", "hello", "python"]
    expected = {"hello": 2, "world": 1, "python": 1}

    # When
    result = count_word_occurences(words)

    # Then
    assert result == expected


def test_counting_with_sorting():
    # Given
    words = ["hello", "world", "hello", "python", "python", "python"]
    expected = {"python": 3, "hello": 2, "world": 1}

    # When
    result = count_word_occurences(words, sort_words=True, reverse=True)

    # Then
    assert result == expected


def test_empty_list():
    # Given
    words = []
    expected = {}

    # When
    result = count_word_occurences(words)

    # Then
    assert result == expected


def test_top_occurrences():
    # Given
    word_occurrences = {
        "hello": 7,
        "world": 5,
        "python": 3,
    }

    expected = [
        {"hello": 7},
        {"world": 5},
        {"python": 3},
    ]

    # When
    result = get_top_word_occurences(word_occurrences)

    # Then
    assert result == expected


def test_handle_count_top_words_occurence(mock_funcs):
    # Given
    mock_clean, mock_words, mock_cleaned_words, mock_count, mock_top = mock_funcs

    mock_clean.return_value = "clean html content"
    mock_words.return_value = ["word1", "word2"]
    mock_cleaned_words.return_value = ["word1", "word2"]
    mock_count.return_value = {"word1": 1, "word2": 1}
    mock_top.return_value = [{"word1": 1}, {"word2": 1}]

    html_content = "<html>content</html>"

    # When
    handle_count_top_words_occurence(html_content)

    # Then
    mock_clean.assert_called_once_with(html_content)
    mock_words.assert_called_once_with("clean html content")
    mock_cleaned_words.assert_called_once_with(["word1", "word2"])
    mock_count.assert_called_once_with(["word1", "word2"], True, True)
    mock_top.assert_called_once_with({"word1": 1, "word2": 1})
