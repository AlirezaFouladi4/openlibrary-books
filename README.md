# OpenLibrary Books Fetcher

A simple Python script that fetches 50 books from the
[OpenLibrary API](https://openlibrary.org/dev/docs/api/search), keeps only those
first published after 2000, and saves them to a CSV file.


The script creates a `books.csv` file in the same folder.

## Output

| Column               | Description                        |
|----------------------|------------------------------------|
| `title`              | Book title                         |
| `authors`            | Authors, separated by `;`          |
| `first_publish_year` | Year of first publication          |
| `openlibrary_url`    | Link to the book on OpenLibrary    |

Rows are sorted by publish year. A sample `books.csv` is included.

## Notes

- 50 books are fetched first, then filtered, so the CSV may have fewer than 50 rows.
- "After 2000" means year > 2000.
- No topic was specified in the task, so a generic search term (`book`) is used.
- Books without a publish year are skipped.
