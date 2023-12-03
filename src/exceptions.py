class ParserFindTagException(Exception):
    """Поднимается, когда парсер не может найти тег."""
    pass


class ListNotFoundException(Exception):
    """Поднимается, если не нашёлся нужный список."""
    pass


class PageNotLoadException(Exception):
    """Поднимается, если основная страница не загрузилась."""
    pass
