import asyncio
import functools
import inspect

from .client import TonlibClient
from .models import Wallet

def _syncify_wrap(t, method_name):
    method = getattr(t, method_name)

    @functools.wraps(method)
    def syncified(*args, **kwargs):
        coro = method(*args, **kwargs)
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return coro
        else:
            return loop.run_until_complete(coro)

    # Save an accessible reference to the original method
    setattr(syncified, '__tl.sync', method)
    setattr(t, method_name, syncified)


def syncify(*types):
    """
    Converts all the methods in the given types (class definitions)
    into synchronous, which return either the coroutine or the result
    based on whether ``asyncio's`` event loop is running.
    """
    # Our asynchronous generators all are `RequestIter`, which already
    # provide a synchronous iterator variant, so we don't need to worry
    # about asyncgenfunction's here.
    for t in types:
        for name in dir(t):
            if not name.startswith('_') or name == '__call__':
                if inspect.iscoroutinefunction(getattr(t, name)):
                    _syncify_wrap(t, name)


syncify(TonlibClient, Wallet)

__all__ = [
    'TonlibClient', 'Wallet'
]