#!/usr/bin/python3

from os import getpid
from dasbus.connection import SystemMessageBus
from .dbdemo_common import DEMO_INTERFACE, DEMO_OBJECT_PATH, ITERATION_REPORT, \
    ITERATION_LIMIT, report_memory, setup_logger


def main():
    logger = setup_logger('dbdemo_client')
    logger.debug('Client PID {}'.format(getpid()))
    bus = SystemMessageBus()
    proxy = bus.get_proxy(DEMO_INTERFACE, DEMO_OBJECT_PATH)

    x = None
    count = 0

    for i in range(ITERATION_LIMIT):
        if count % ITERATION_REPORT == 0:
            report_memory(count)
        count += 1
        x = proxy.GetData('something')
    logger.debug('Final memory report')
    report_memory(count)
    logger.debug(str(x))


if __name__ == '__main__':
    main()
