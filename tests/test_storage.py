import json
import pytest

from librarycatalog.catalog import Catalog
from librarycatalog.errors import CorruptedFileError, UnsupportedVersionError
from librarycatalog.models import make_book
from librarycatalog.storage import load_catalog, save_catalog


def test_round_trip(tmp_path):
    c = Catalog()
    c.add(make_book("1", "War and Peace", "fiction", 1869, "Tolstoy", "AST"))
    c.add(make_book("2", "Anna Karenina", "fiction", 1877, "Tolstoy", "AST"))

    path = tmp_path / "catalog.json"
    save_catalog(c, path)

    c2 = Catalog()
    load_catalog(c2, path)

    assert len(c2) == 2
    assert c2.get("1").title == "War and Peace"


def test_corrupted_json(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text("не json", encoding="utf-8")

    c = Catalog()
    with pytest.raises(CorruptedFileError):
        load_catalog(c, path)
    assert len(c) == 0


def test_unknown_version(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps({"format_version": 999, "books": []}),
        encoding="utf-8",
    )

    c = Catalog()
    with pytest.raises(UnsupportedVersionError):
        load_catalog(c, path)


def test_no_partial_change_on_bad_book(tmp_path):
    c = Catalog()
    c.add(make_book("1", "Existing", "fiction", 2000, "A", "P"))

    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps({
            "format_version": 1,
            "books": [
                {"id": "2", "title": "OK", "category": "fiction",
                 "year": 2001, "author": "B", "publisher": "P"},
                {"id": "3", "title": "", "category": "fiction",
                 "year": 2002, "author": "C", "publisher": "P"},
            ],
        }),
        encoding="utf-8",
    )

    with pytest.raises(CorruptedFileError):
        load_catalog(c, path)

    assert len(c) == 1
    assert "2" not in c
    assert "1" in c