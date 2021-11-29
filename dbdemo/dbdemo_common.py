from dasbus.connection import SystemMessageBus
from dasbus.identifier import DBusServiceIdentifier
from posixpath import sep as posix_sep
from os import getpid
import re

SYSTEM_BUS = SystemMessageBus()
DEMO_NAMESPACE_OBJ = ('com', 'example', 'demo')
DEMO_INTERFACE = '.'.join(DEMO_NAMESPACE_OBJ)
DEMO_OBJECT_PATH = posix_sep + posix_sep.join(DEMO_NAMESPACE_OBJ)

ITERATION_REPORT = 500
ITERATION_LIMIT = 10000

PROCFILE_FMT = '/proc/{}/statm'

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
    print('PID: {}  count={}  size={}  resident={}  shared={}  text={}  '
          'data={}'.format(pid, count, items[0], items[1], items[2], items[3],
                           items[5]))
