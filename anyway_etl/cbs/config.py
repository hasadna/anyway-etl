import os

from ..config import ANYWAY_ETL_DATA_ROOT_PATH


CBS_DATA_ROOT_PATH = os.path.join(ANYWAY_ETL_DATA_ROOT_PATH, 'cbs')
CBS_EMAILS_DATA_ROOT_PATH = os.path.join(CBS_DATA_ROOT_PATH, 'emails')
CBS_FILES_ROOT_PATH = os.path.join(CBS_DATA_ROOT_PATH, 'files')
CBS_YEARLY_DIRECTORIES_ROOT_PATH = os.path.join(CBS_DATA_ROOT_PATH, 'yearly')
CBS_ACCIDENT_MARKERS_ROOT_PATH = os.path.join(CBS_DATA_ROOT_PATH, 'accident_markers')
CBS_INVOLVED_ROOT_PATH = os.path.join(CBS_DATA_ROOT_PATH, 'involved')
CBS_VEHICLES_ROOT_PATH = os.path.join(CBS_DATA_ROOT_PATH, 'vehicles')

IMAP_MAIL_DIR = os.environ.get('IMAP_MAIL_DIR', "cbs/data")
IMAP_MAIL_USER = os.environ.get('IMAP_MAIL_USER')
IMAP_MAIL_PASSWORD = os.environ.get('IMAP_MAIL_PASSWORD')
IMAP_MAIL_HOST = os.environ.get('IMAP_MAIL_HOST', "imap.gmail.com")

PREPROCESS_FILES_DEFAULT_LIMIT_ROWS = int(os.environ.get('PREPROCESS_FILES_DEFAULT_LIMIT_ROWS', '2'))
