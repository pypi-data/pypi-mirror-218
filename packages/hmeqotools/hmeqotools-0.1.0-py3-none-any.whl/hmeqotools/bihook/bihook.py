import PyHook3

from .event import *

hook_manager: PyHook3.HookManager = None  # type: ignore


def _exc_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            on_error(exc)
        return True
    return wrapper


class Keyboard:

    _hook = False

    @classmethod
    def hook(cls):
        if not cls._hook:
            cls._hook = True
            hook_manager.KeyAll = cls.on_event
            hook_manager.HookKeyboard()

    @classmethod
    def unhook(cls):
        if cls._hook:
            cls._hook = False
            hook_manager.UnhookKeyboard()
            hook_manager.KeyAll = None

    @staticmethod
    @_exc_catcher
    def on_event(event):
        message = event.Message
        kid = event.KeyID
        if message in ALLKEYDOWN:
            events.set_event(kid, event)
            if is_sys_protected_key(get_combination()):
                bind.emit(SYSPROTECTED)
                events.clear()
                return bind.prevention_code
            bind.emit(ALLKEYDOWN, event)
            if bind.is_prevented():
                return bind.prevention_code
            bind.emit(message, event)
        elif message in ALLKEYUP:
            events.remove_event(kid)
            bind.emit(ALLKEYUP, event)
            if bind.is_prevented():
                return bind.prevention_code
            bind.emit(message, event)
        elif message in ALLCHAR:
            bind.emit(ALLCHAR, event)
            if bind.is_prevented():
                return bind.prevention_code
            bind.emit(message, event)
        elif message in ALLDEADCHAR:
            bind.emit(ALLDEADCHAR, event)
            if bind.is_prevented():
                return bind.prevention_code
            bind.emit(message, event)
        if bind.is_prevented():
            events.remove_event(kid)
            return bind.prevention_code

        if kid in K_CONTROL:
            bind.emit(K_CONTROL, event)
        elif kid in K_SHIFT:
            bind.emit(K_SHIFT, event)
        elif kid in K_ALT:
            bind.emit(K_ALT, event)
        elif kid in K_WIN:
            bind.emit(K_WIN)
        if bind.is_prevented():
            events.remove_event(kid)
            return bind.prevention_code

        bind.emit(kid, event)
        if bind.is_prevented():
            events.remove_event(kid)
        return bind.prevention_code


class Mouse:

    _hook = False
    pos = (0, 0)

    @classmethod
    def hook(cls):
        if not cls._hook:
            cls._hook = True
            hook_manager.MouseAll = cls.on_event
            hook_manager.HookMouse()

    @classmethod
    def unhook(cls):
        if cls._hook:
            cls._hook = False
            hook_manager.UnhookMouse()
            hook_manager.MouseAll = None

    @classmethod
    @_exc_catcher
    def on_event(cls, event):
        message = event.Message
        if message == MOUSEMOVE:
            cls.pos = event.Position
        bind.emit(message, event)
        return bind.prevention_code


def hook(keyboard=False, mouse=False):
    global hook_manager
    if hook_manager is None:
        hook_manager = PyHook3.HookManager()
    if keyboard:
        Keyboard.hook()
    if mouse:
        Mouse.hook()


def unhook():
    Keyboard.unhook()
    Mouse.unhook()
