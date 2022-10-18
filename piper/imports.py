import builtins
import inspect
from types import ModuleType

from piper.utils.logger_utils import logger
from piper.configurations import get_configuration

configuration = get_configuration()


def _empty_import():
    logger.error("Import Not Installed Yet!")
    raise ImportError


real_import = _empty_import


class PiperDummyModule(ModuleType):

    def __init__(self, name):
        super().__init__(name)
        logger.info(f"Piper emulates {name} module")

    def __getattr__(self, name):
        return PiperDummyModule(name)

    __all__ = []


def try_import(name, globals={}, locals={}, fromlist=[], level=0):
    """
    This import replace real Python import with fake import which returns warning only and PiperDummyModule.
    This works for everything under piper/ frameworks files by filename but not for piper import (like piper.base)
    And this also works for every file where you import something from piper firstly !
    """
    is_piper_imported_from_previous_module = False
    prev_module_locals = inspect.currentframe().f_back.f_locals
    prev_module_globals = inspect.currentframe().f_back.f_globals
    prev_modules = prev_module_locals | prev_module_globals

    if prev_modules.values():
        prev_modules = [v for v in prev_modules.values() if v is not None and hasattr(v, "__module__")]
        if len(prev_modules) > 0:
            is_piper_imported_from_previous_module = \
                any("piper" in v.__module__ for v in prev_modules if type(v.__module__) == str)

    is_import_from_piper_source_code = "__file__" in globals and "piper/" in globals["__file__"]
    not_piper_import = not ("piper" in name)
    is_from_source_but_not_piper = is_import_from_piper_source_code and not_piper_import

    if is_piper_imported_from_previous_module and is_from_source_but_not_piper:
        logger.info(f"Piper activates safe import for library {name} in piper file {globals['__file__']} ")
        try:
            return real_import(name, globals, locals, fromlist, level)
        except ImportError as e:
            logger.warning(f"Piper ignores ImportError and module {name} "
                           f": replaced by dummy module. ImportError: {e.with_traceback(None)}")
            module = PiperDummyModule(name)
            return module
    else:
        return real_import(name, globals, locals, fromlist, level)


"""
Here Piper saves default Python *import* only.
"""
if builtins.__import__ != try_import:
    real_import = builtins.__import__


def set_ignore_import_errors(ignore: bool = True):
    if ignore:
        builtins.__import__ = try_import
    else:
        builtins.__import__ = real_import


def activate_safe_import():
    """
    Activate piper safe import with try_import function.
    Piper needs safe import to ignore imports in Executors examples.
    For instance if you want to use Pandas in your CustomExecutor normally you have to *import pandas*
    But we don't want to install everything for every executor in default Python (where Piper is installed)
    For that you have to ignore every Executors dependencies.

    Otherwise, you can wrap buy yourself every Executors import with try_import
    or you can use directly only *requirements* field in your CustomExecutor.

    """
    logger.info(f"Piper activates safe import")
    set_ignore_import_errors(ignore=True)


def deactivate_safe_import():
    logger.info(f"Piper deactivates safe import")
    set_ignore_import_errors(ignore=False)


class safe_import:
    """
    Context manager to activate safe import on some part of imports.
    For instance:

        with safe_import():
            import foo
        import bar

    foo would be ignored and replaced by PiperDummyModule
    boo wouldn't be replaced (you can catch ImportError)
    """

    def __enter__(self):
        activate_safe_import()

    def __exit__(self, type, value, traceback):
        deactivate_safe_import()
