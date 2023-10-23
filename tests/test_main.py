from unittest.mock import patch

from src.main import main


# Given
@patch("src.main.open_results")
@patch("src.main.generate_and_save_results")
@patch("src.main.get_most_frequent_words_from_url")
@patch("src.main.open_page_from_url")
@patch("builtins.input", return_value="http://example.com")
def test_main(
    mock_input,
    mock_open_page_from_url,
    mock_get_most_frequent_words_from_url,
    mock_generate_and_save_results,
    mock_open_results,
):
    # When
    main()

    # Then
    mock_input.assert_called_once_with("Please enter a URL: ")
    mock_open_page_from_url.assert_called_once_with("http://example.com")
    mock_get_most_frequent_words_from_url.assert_called_once_with("http://example.com")
    mock_generate_and_save_results.assert_called_once()
    mock_open_results.assert_called_once()
