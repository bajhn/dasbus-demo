import signal
from gi.repository import GLib
from dasbus.server.interface import dbus_interface
from dasbus.typing import Structure, Variant, Str
from .demo_common import DEMO_SERVICE_ID, SYSTEM_BUS, ITERATION_REPORT, \
    report_memory
from base64 import b64encode

from os import urandom, getpid


count = 0


@dbus_interface(DEMO_SERVICE_ID.interface_name)
class DemoServer(object):

    # append some random padding to name so we can see the memory increase in top.
    # noinspection PyPep8Naming
    def GetData(self, name: Str) -> Str:
        global count

        if count % ITERATION_REPORT == 0:
            report_memory(count)
        count += 1
        return '{}: pid={}, data={}'.format(name, getpid(),
                                            b64encode(urandom(1024)).decode('utf-8'))


def init_dbus_service() -> DemoServer:
    server = DemoServer()
    SYSTEM_BUS.publish_object(DEMO_SERVICE_ID.object_path,
                              server)
    SYSTEM_BUS.register_service(DEMO_SERVICE_ID.service_name)
    # Caller needs to initialize and run the event loop.
    return server


def signal_handler(loop):
    print('Signal handler terminating main loop.')
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
    print('Server PID {}'.format(getpid()))
    report_memory(count)
    d = init_dbus_service()
    # noinspection PyUnresolvedReferences
    main_loop.run()


if __name__ == '__main__':
    main()
