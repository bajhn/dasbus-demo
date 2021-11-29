import logging

from dasbus.connection import SystemMessageBus
from dasbus.identifier import DBusServiceIdentifier
from posixpath import sep as posix_sep
from os import getpid
import re

# DEBUG_FORMAT = '%(asctime)s %(process)d %(threadName)s %(funcName)s[%(lineno)d] %(message)s'
LOG_FORMAT = '%(asctime)s %(process)d %(message)s'
SYSTEM_BUS = SystemMessageBus()
DEMO_NAMESPACE_OBJ = ('com', 'example', 'dbdemo')
DEMO_INTERFACE = '.'.join(DEMO_NAMESPACE_OBJ)
DEMO_OBJECT_PATH = posix_sep + posix_sep.join(DEMO_NAMESPACE_OBJ)

ITERATION_REPORT = 500
ITERATION_LIMIT = 10000

PROCFILE_FMT = '/proc/{}/statm'

logger = logging.getLogger(__name__)

DEMO_SERVICE_ID = DBusServiceIdentifier(
    namespace=DEMO_NAMESPACE_OBJ,
    message_bus=SYSTEM_BUS
)


def report_memory(count):
    pid = getpid()
    data = open(PROCFILE_FMT.format(pid)).readline()
    items = re.findall(r'(\d+)', data)
    assert len(items) == 7
    # Contents of proc file are:
    # size  resident  shared  text  lib(0)  data  dt(0)
    # man reports that resident and shared values are inaccurate.
    logger.debug('PID={} count={}  size={}  resident={}  shared={}  text={} '
                 'data={}'.format(pid, count, items[0], items[1], items[2],
                                  items[3], items[5]))


def setup_logger(name: str) -> logging.Logger:
    logging.name = name
    logging.root.setLevel(logging.DEBUG)
    handler = logging.FileHandler('/tmp/{}.log'.format(name),
                                  mode='a', encoding='utf-8')
    handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
    logging.root.addHandler(handler)
    return logging.getLogger(name)
