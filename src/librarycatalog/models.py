from dataclasses import dataclass

from .errors import InvalidBookError

CATEGORIES = [
    "fiction",
    "non-fiction",
    "science",
    "history",
    "poetry",
    "children",
]


@dataclass
class Book:
    id: str
    title: str
    category: str
    year: int
    author: str
    publisher: str


def make_book(id, title, category, year, author, publisher):
    """Создаёт и валидирует книгу. Неверная — исключение."""
    if not isinstance(id, str) or id == "":
        raise InvalidBookError("id must be non-empty string")

    if not isinstance(title, str) or title == "":
        raise InvalidBookError("title must be non-empty string")

    if category not in CATEGORIES:
        raise InvalidBookError("invalid category: " + str(category))

    if not isinstance(year, int) or year < 1000 or year > 2100:
        raise InvalidBookError("invalid year: " + str(year))

    if not isinstance(author, str) or author == "":
        raise InvalidBookError("author must be non-empty string")

    if not isinstance(publisher, str) or publisher == "":
        raise InvalidBookError("publisher must be non-empty string")

    return Book(
        id=id,
        title=title,
        category=category,
        year=year,
        author=author,
        publisher=publisher,
    )


def book_to_dict(book):
    return {
        "id": book.id,
        "title": book.title,
        "category": book.category,
        "year": book.year,
        "author": book.author,
        "publisher": book.publisher,
    }


def book_from_dict(data):
    return make_book(
        data["id"],
        data["title"],
        data["category"],
        data["year"],
        data["author"],
        data["publisher"],
    )