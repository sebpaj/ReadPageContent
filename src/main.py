from src.core import (
    generate_and_save_results,
    get_most_frequent_words_from_url,
    open_page_from_url,
    open_results,
)


def main():
    url = input("Please enter a URL: ")

    open_page_from_url(url)

    most_frequent_words = get_most_frequent_words_from_url(url)

    generate_and_save_results(most_frequent_words)

    open_results()


if __name__ == "__main__":
    main()
