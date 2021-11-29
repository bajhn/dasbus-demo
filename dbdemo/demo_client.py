#!/usr/bin/python3

import time
from os import getpid
from dasbus.connection import SystemMessageBus
from .demo_common import DEMO_INTERFACE, DEMO_OBJECT_PATH, ITERATION_REPORT, \
    ITERATION_LIMIT, report_memory

print('Client PID {}'.format(getpid()))
bus = SystemMessageBus()
time.sleep(30)
proxy = bus.get_proxy(DEMO_INTERFACE, DEMO_OBJECT_PATH)

x = None
count = 0

for i in range(ITERATION_LIMIT):
    if count % ITERATION_REPORT == 0:
        report_memory(count)
    count += 1
    x = proxy.GetData('something')
report_memory(count)
print(x)
