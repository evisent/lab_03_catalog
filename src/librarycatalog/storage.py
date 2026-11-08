import json

from .catalog import Catalog
from .errors import CorruptedFileError, UnsupportedVersionError
from .models import book_from_dict, book_to_dict

FORMAT_VERSION = 1


def save_catalog(catalog, path):
    data = {
        "format_version": FORMAT_VERSION,
        "books": [book_to_dict(book) for book in catalog],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_catalog(catalog, path):
    """Загружает книги в существующий каталог"""
    
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise CorruptedFileError("cannot read file: " + str(e))

    if not isinstance(data, dict):
        raise CorruptedFileError("top-level must be object")

    version = data.get("format_version")
    if version != FORMAT_VERSION:
        raise UnsupportedVersionError("unsupported format_version: " + str(version))

    raw_books = data.get("books")
    if not isinstance(raw_books, list):
        raise CorruptedFileError("books must be list")

    parsed = []
    for raw in raw_books:
        try:
            parsed.append(book_from_dict(raw))
        except Exception as e:
            raise CorruptedFileError("bad book: " + str(e))

    for book in parsed:
        if book.id in catalog:
            raise CorruptedFileError("duplicate id in file: " + book.id)

    for book in parsed:
        catalog.add(book)