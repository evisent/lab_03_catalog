class CatalogError(Exception):
    pass


class InvalidBookError(CatalogError):
    pass


class DuplicateIdError(CatalogError):
    pass


class BookNotFoundError(CatalogError):
    pass


class UnsupportedVersionError(CatalogError):
    pass


class CorruptedFileError(CatalogError):
    pass