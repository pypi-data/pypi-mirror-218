import signal
import atexit
import sys
from threading import Event, RLock
from typing import Set, Optional


# BE WARNED: this package uses signals so must be imported first from the main thread


cancel_events: Set[Event] = set()
cancel_events_lock = RLock()
original_sigint_handler = signal.getsignal(signal.SIGINT)
original_exception_handler = sys.excepthook


def _cancel_all_and_stop_registering() -> None:
    global cancel_events
    # try to atomically turn off possibility of registering new events during this call
    # but in a very rare case though this can lead to "invoking method on a None object error" in functions:
    # register_cancellable | unregister_cancellable
    # but this does not matter because we are shutting down
    # and because we are shutting down then i do not want to use locking here
    alias_cancel_events = cancel_events
    cancel_events = None
    if alias_cancel_events is not None:
        for event in alias_cancel_events:
            event.set()


def handle_sigint(signum, frame):
    _cancel_all_and_stop_registering()
    original_sigint_handler(signum, frame)


def handle_exit():
    _cancel_all_and_stop_registering()


def handle_exception(exctype, value, tb):
    _cancel_all_and_stop_registering()
    if original_exception_handler is not None:
        original_exception_handler(exctype, value, tb)


signal.signal(signal.SIGINT, handle_sigint)
atexit.register(handle_exit)
sys.excepthook = handle_exception


def register_cancellable(event: Event = None) -> Optional[Event]:
    if cancel_events is not None:
        event = event if event is not None else Event()
        with cancel_events_lock:
            cancel_events.add(event)
        return event


def unregister_cancellable(event: Event) -> None:
    if cancel_events is not None and event in cancel_events:
        with cancel_events_lock:
            cancel_events.discard(event)
