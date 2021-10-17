import inspect
import logging
import traceback
import functools

def log(func):
        @functools.wraps(func)
        def callf(*args, **kwargs):
            logger = logging.getLogger('server.main')
            logger.debug("Вызов %s: %s, %s" % (func.__name__, args, kwargs))
            logger.debug(f"функция {func.__name__} вызвана из функции {inspect.stack()[1][3]}")
            r = func(*args, **kwargs)
            logger.debug("%s вернула %s" % (func.__name__, r))
            return r
        return callf
