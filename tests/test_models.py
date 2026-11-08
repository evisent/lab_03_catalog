import pytest

from librarycatalog.errors import InvalidBookError
from librarycatalog.models import make_book


def test_make_book_ok():
    book = make_book("1", "War and Peace", "fiction", 1869, "Tolstoy", "978-5-04-116640-2")
    assert book.id == "1"
    assert book.title == "War and Peace"
    assert book.author == "Tolstoy"


def test_empty_id():
    with pytest.raises(InvalidBookError):
        make_book("", "X", "fiction", 2000, "A", "123")


def test_bad_year():
    with pytest.raises(InvalidBookError):
        make_book("1", "X", "fiction", 500, "A", "123")


def test_bad_category():
    with pytest.raises(InvalidBookError):
        make_book("1", "X", "banana", 2000, "A", "123")


def test_empty_author():
    with pytest.raises(InvalidBookError):
        make_book("1", "X", "fiction", 2000, "", "123")


def test_empty_isbn():
    with pytest.raises(InvalidBookError):
        make_book("1", "X", "fiction", 2000, "A", "")