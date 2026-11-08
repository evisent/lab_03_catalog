import pytest

from librarycatalog.catalog import Catalog
from librarycatalog.errors import BookNotFoundError, DuplicateIdError
from librarycatalog.models import make_book


def test_add_get():
    c = Catalog()
    book = make_book("1", "War and Peace", "fiction", 1869, "Tolstoy", "AST")
    c.add(book)
    assert c.get("1") is book
    assert len(c) == 1


def test_duplicate():
    c = Catalog()
    book = make_book("1", "X", "fiction", 2000, "A", "P")
    c.add(book)
    with pytest.raises(DuplicateIdError):
        c.add(book)


def test_remove():
    c = Catalog()
    c.add(make_book("1", "X", "fiction", 2000, "A", "P"))
    c.remove("1")
    assert len(c) == 0
    with pytest.raises(BookNotFoundError):
        c.remove("1")


def test_find_by_category():
    c = Catalog()
    c.add(make_book("1", "A", "fiction", 2000, "X", "P1"))
    c.add(make_book("2", "B", "science", 2001, "Y", "P2"))
    c.add(make_book("3", "C", "fiction", 2002, "Z", "P3"))
    result = c.find_by_category("fiction")
    assert len(result) == 2
    assert {b.id for b in result} == {"1", "3"}


def test_find_by_name_case_insensitive():
    c = Catalog()
    c.add(make_book("1", "War and Peace", "fiction", 1869, "Tolstoy", "AST"))
    c.add(make_book("2", "Anna Karenina", "fiction", 1877, "Tolstoy", "AST"))
    assert len(c.find_by_name("WAR")) == 1
    assert len(c.find_by_name("war")) == 1


def test_iteration_order():
    c = Catalog()
    c.add(make_book("b", "B", "fiction", 2000, "A", "P"))
    c.add(make_book("a", "A", "fiction", 2000, "A", "P"))
    c.add(make_book("c", "C", "fiction", 2000, "A", "P"))
    ids = [book.id for book in c]
    assert ids == ["a", "b", "c"]


def test_contains():
    c = Catalog()
    c.add(make_book("1", "X", "fiction", 2000, "A", "P"))
    assert "1" in c
    assert "2" not in c


def test_find_returns_new_list():
    c = Catalog()
    c.add(make_book("1", "X", "fiction", 2000, "A", "P"))
    result = c.find_by_category("fiction")
    result.clear()
    assert len(c) == 1