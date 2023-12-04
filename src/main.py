import re
import logging
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR, MAIN_DOC_URL, PEP_DOC_URL, FEATURES,
    EXPECTED_STATUS, QUANTITY_STATUS, PATTERN
)
from exceptions import ListNotFoundException
from outputs import control_output
from utils import get_response, find_tag, get_soup


def whats_new(session):
    """
    Парсер ссылок на статьи о нововведениях в Python.
    И информации об авторах и редакторах статей.
    """
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url, FEATURES)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]

    for section in tqdm(sections_by_python):
        version_link = urljoin(whats_new_url, section.find('a')['href'])
        response = get_response(session, version_link)

        if response is None:
            continue

        soup = BeautifulSoup(response.text, features=FEATURES)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    """Парсер данных актуальных версий Python."""
    soup = get_soup(session, MAIN_DOC_URL, FEATURES)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ListNotFoundException('Ничего не нашлось')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = PATTERN

    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )

    return results


def download(session):
    """Парсер, который скачивает архив с документацией Python."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url, FEATURES)
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    archive_url = urljoin(downloads_url, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = get_response(session, archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    """Парсинг документов PEP."""
    soup = get_soup(session, PEP_DOC_URL, FEATURES)
    main_div = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    pep_number = main_div.find_all('a', {'class': 'pep reference internal'})
    pep_status = main_div.find_all('abbr')
    status_count = 0
    set_pep = set()
    results = [('Статус', 'Количество')]

    for i in pep_number:
        set_pep.add(i['href'])

    for i in tqdm(pep_number):
        if i['href'] in set_pep:
            set_pep.discard(i['href'])
        else:
            continue

        index_status = pep_status[status_count].text[1:]
        
        this_status = EXPECTED_STATUS[index_status]
        version_pep = urljoin(PEP_DOC_URL, i['href'])
        response = get_response(session, version_pep)
        
        if response is None:
            continue
        
        soup = BeautifulSoup(response.text, features=FEATURES)
        abbr = find_tag(soup, 'abbr')
        status_count += 1
        if abbr.text in this_status:
            if abbr.text in QUANTITY_STATUS:
                QUANTITY_STATUS[abbr.text] += 1
            else:
                QUANTITY_STATUS[abbr.text] = 1
            QUANTITY_STATUS['Total'] += 1
        else:
            not_status = (
                '\nНесовпадающие статусы:\n'
                f'{version_pep}\n'
                f'Статус в карточке: {abbr.text}\n'
                f'Ожидаемые статусы: {EXPECTED_STATUS[index_status]}\n'
            )
            logging.info(not_status)
    for key, value in QUANTITY_STATUS.items():
        results.append((key, value))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    """Главная функция."""
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()

    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results:
        control_output(results, args)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
