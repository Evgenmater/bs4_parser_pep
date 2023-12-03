import logging

from bs4 import BeautifulSoup

from requests import RequestException
from exceptions import ParserFindTagException, PageNotLoadException


def get_response(session, url):
    """Перехват ошибки при загрузке страницы."""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def get_soup(session, url, feature):
    try:
        response = get_response(session, url)
    except PageNotLoadException:
        logging.exception(
            f'Основная страница {url} не загрузилась',
            stack_info=True
        )
    return BeautifulSoup(response.text, features=feature)


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки поиска тегов."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
