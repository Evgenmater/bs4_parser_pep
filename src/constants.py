from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'
BASE_DIR = Path(__file__).parent
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
PRETTY = 'pretty'
FILE = 'file'
FEATURES = 'lxml'

# Регулярное выражение для поиска номера версии и
# статуса версии Python, текста в скобках.
PATTERN = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

QUANTITY_STATUS = {'Total': 0}
