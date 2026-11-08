from .errors import BookNotFoundError, DuplicateIdError


class Catalog:
    def __init__(self):
        self._items = {}

    def add(self, book):
        if book.id in self._items:
            raise DuplicateIdError("duplicate id: " + book.id)
        self._items[book.id] = book

    def get(self, item_id):
        if item_id not in self._items:
            raise BookNotFoundError("not found: " + item_id)
        return self._items[item_id]

    def remove(self, item_id):
        if item_id not in self._items:
            raise BookNotFoundError("not found: " + item_id)
        del self._items[item_id]

    def find_by_category(self, category):
        result = []
        for book in self._items.values():
            if book.category == category:
                result.append(book)
        return result

    def find_by_name(self, query):
        result = []
        query_lower = query.lower()
        for book in self._items.values():
            if query_lower in book.title.lower():
                result.append(book)
        return result

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        for book_id in sorted(self._items):
            yield self._items[book_id]

    def __contains__(self, item_id):
        return item_id in self._items
