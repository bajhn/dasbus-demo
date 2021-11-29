import signal
from gi.repository import GLib
from dasbus.server.interface import dbus_interface
from dasbus.typing import Str
from .dbdemo_common import DEMO_SERVICE_ID, SYSTEM_BUS, ITERATION_REPORT, \
    report_memory, setup_logger
from base64 import b64encode
from os import urandom, getpid

bus = None
logger = setup_logger('dbdemo_server')
REPORTING_TIME_LIMIT = 180  # Stop logging memory reports after this limit.
DELAY = 5
STATIC_STRING = 'See the quick brown fox jump over the lazy dog.' * 22


@dbus_interface(DEMO_SERVICE_ID.interface_name)
class DemoServer(object):

    def __init__(self):
        self.count = 0

    # Append some random padding to name so we can see the memory increase in
    # top. Random padding is used so that Python doesn't reuse the same object
    # for the input value.
    # noinspection PyPep8Naming,PyMethodMayBeStatic
    def GetData(self, name: Str) -> Str:
        if self.count % ITERATION_REPORT == 0:
            report_memory(self.count)
        self.count += 1
        # return STATIC_STRING
        return '{}: data={}'.format(name, b64encode(urandom(1024)).decode('utf-8'))


def init_dbus_service() -> DemoServer:
    server = DemoServer()
    SYSTEM_BUS.publish_object(DEMO_SERVICE_ID.object_path,
                              server)
    SYSTEM_BUS.register_service(DEMO_SERVICE_ID.service_name)
    # Caller needs to initialize and run the event loop.
    return server


def signal_handler(loop):
    logger.debug('Signal handler terminating main loop.')
    loop.quit()


def main():
    global bus

    main_loop = GLib.MainLoop()
    GLib.unix_signal_add(
        GLib.PRIORITY_HIGH, signal.SIGHUP, signal_handler, main_loop)
    GLib.unix_signal_add(
        GLib.PRIORITY_HIGH, signal.SIGTERM, signal_handler, main_loop)
    GLib.unix_signal_add(
        GLib.PRIORITY_HIGH, signal.SIGINT, signal_handler, main_loop)
    logger.debug('Server PID {}'.format(getpid()))
    # noinspection PyUnusedLocal
    d = init_dbus_service()
    # noinspection PyUnresolvedReferences
    main_loop.run()


if __name__ == '__main__':
    main()
