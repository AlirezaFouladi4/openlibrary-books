"""Fetch 50 books from the OpenLibrary API, keep only the ones first
published after 2000, and save them to a CSV file."""

import csv

import requests

API_URL = "https://openlibrary.org/search.json"
BASE_URL = "https://openlibrary.org"
SEARCH_QUERY = "book"  # generic term: the task does not specify a topic
BOOKS_TO_FETCH = 50
YEAR_THRESHOLD = 2000  # keep books published strictly after this year
REQUEST_TIMEOUT = 10  # seconds
OUTPUT_FILE = "books.csv"
CSV_COLUMNS = ["title", "authors", "first_publish_year", "openlibrary_url"]


def fetch_books(limit):
    """Request `limit` books from OpenLibrary and return them as a list of dicts."""
    params = {
        "q": SEARCH_QUERY,
        "fields": "key,title,author_name,first_publish_year",
        "limit": limit,
    }
    response = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()  # stop with a clear error on 4xx/5xx responses
    return response.json()["docs"]


def filter_books_after_year(books, year):
    """Return only the books whose first publish year is greater than `year`.

    Books without a publish year are skipped.
    """
    filtered_books = []
    for book in books:
        publish_year = book.get("first_publish_year")
        if publish_year is not None and publish_year > year:
            filtered_books.append(book)
    return filtered_books


def book_to_row(book):
    """Convert a raw API book dict into a flat dict matching CSV_COLUMNS."""
    authors = book.get("author_name", [])
    return {
        "title": book.get("title", ""),
        "authors": "; ".join(authors),
        "first_publish_year": book["first_publish_year"],
        "openlibrary_url": BASE_URL + book.get("key", ""),
    }


def save_to_csv(books, file_path):
    """Write the books to a CSV file, sorted by publish year (oldest first)."""
    rows = [book_to_row(book) for book in books]
    rows.sort(key=lambda row: row["first_publish_year"])


    with open(file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    try:
        books = fetch_books(BOOKS_TO_FETCH)
    except requests.RequestException as error:
        print(f"Failed to fetch data from OpenLibrary: {error}")
        return

    print(f"Fetched {len(books)} books.")

    recent_books = filter_books_after_year(books, YEAR_THRESHOLD)
    print(f"{len(recent_books)} books were first published after {YEAR_THRESHOLD}.")

    save_to_csv(recent_books, OUTPUT_FILE)
    print(f"Saved results to {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
