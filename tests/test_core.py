from unittest.mock import mock_open, patch, call

import pytest

from src.core import (
    generate_and_save_results,
    get_most_frequent_words_from_url,
    open_page_from_url,
    open_results,
)


@patch("webbrowser.open")
def test_open_page_from_url(mock_patch):
    # Given
    test_url = "http://example.com"

    # When
    open_page_from_url(test_url)

    # Then
    mock_patch.assert_called_once_with(test_url)


@patch("src.core.handle_count_top_words_occurence")
@patch("src.core.get_html_content")
def test_get_most_frequent_words_from_url_success(
    mock_get_html_content, mock_handle_count
):
    # Given
    test_url = "http://example.com"
    test_html_content = "<html>content</html>"
    test_top_words = [{"word1": 1}, {"word2": 2}]

    mock_get_html_content.return_value = test_html_content
    mock_handle_count.return_value = test_top_words

    # When
    result = get_most_frequent_words_from_url(test_url)

    # Then
    assert result == test_top_words
    mock_get_html_content.assert_called_once_with(test_url)
    mock_handle_count.assert_called_once_with(test_html_content)


@patch("src.core.get_html_content")
def test_get_most_frequent_words_from_url_failure(mock_get_html_content):
    # Given
    test_url = "http://example.com"

    mock_get_html_content.return_value = None

    # When & Then
    with pytest.raises(ValueError, match="Could not get html data"):
        get_most_frequent_words_from_url(test_url)


def test_generate_and_save_results():
    # Given
    top_words_occurence = [{"word1": 1}, {"word2": 2}]

    # When
    mocked_file = mock_open()
    with patch("builtins.open", mocked_file):
        generate_and_save_results(top_words_occurence)

    # Then
    mocked_file.assert_any_call("../result.html", "w")
    mocked_file.assert_any_call("../result.txt", "w")


@patch("src.core.webbrowser.open")
@patch("src.core.os.path.abspath")
def test_open_results(mock_os_path_abspath, mock_webbrowser_open):
    # Given
    mock_os_path_abspath.return_value = "/absolute/path/to/result.html"

    # When
    open_results()

    # Then
    mock_os_path_abspath.assert_called_once_with("../result.html")
    mock_webbrowser_open.assert_called_once_with("file:///absolute/path/to/result.html")
