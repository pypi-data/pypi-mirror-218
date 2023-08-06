import traceback
from collections import defaultdict
from typing import Callable

from .const import *
from .combination import Combination

sys_pretected_combinations = [
    CTRL_ALT_DEL,
    CTRL_SHIFT_ESC,
]


def on_error(exc: Exception):
    print(
        "--------------------------------------------------"
        + "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        + "--------------------------------------------------"
    )


def is_sys_protected_key(key):
    return key in sys_pretected_combinations


class Events:

    def __init__(self):
        self.events = {}

    def get_combination(self):
        if not self.events:
            return NUL_COMBINATION
        return Combination(
            iter_=(i.KeyID for i in sorted(
                self.events.values(), key=lambda x: x.Time)),
            order=True,
        )

    def set_event(self, key, event):
        self.events[key] = event

    def remove_event(self, key):
        if key in self.events:
            del self.events[key]

    def clear(self):
        self.events.clear()


class Bind:

    def __init__(self):
        self.subscribers = defaultdict(list)
        self.prevented = False
        self.prevention_code = True

    def subscribe(self, key, subscriber: Callable):
        self.subscribers[key].append(subscriber)

    def unsubscribe(self, key, subscriber: Callable):
        try:
            self.subscribers[key].remove(subscriber)
        except Exception as exc:
            on_error(exc)

    def emit(self, key, *args, **kwargs):
        self.prevented = False
        self.prevention_code = True
        for func in self.subscribers[key]:
            func(*args, **kwargs)
            if self.is_prevented():
                break

    def prevent(self, code=True):
        self.prevented = True
        self.prevention_code = code

    def is_prevented(self):
        return self.prevented

    __call__ = subscribe


bind = Bind()
events = Events()
prevent = bind.prevent
get_combination = events.get_combination
