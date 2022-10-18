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


def _piper_was_touched_in_frame(frame_before=1):
    call_function_frame = inspect.currentframe().f_back
    frame = call_function_frame
    for i in range(frame_before):
        frame = frame.f_back

    result = False
    f_locals = frame.f_locals
    f_globals = frame.f_globals
    all_variables = f_locals | f_globals

    if all_variables.values():
        all_variables = [v for v in all_variables.values() if v is not None]
        if len(all_variables) > 0:
            variables_have_piper_package = any("piper" in v.__package__ \
                    for v in all_variables if hasattr(v, "__package__") and type(v.__package__) == str)
            variables_have_piper_module = any("piper" in v.__module__ \
                    for v in all_variables if hasattr(v, "__module__") and type(v.__module__) == str)
            result = variables_have_piper_module | variables_have_piper_package

    return result


def _from_piper_file_but_not_piper(name: str, globals={}):
    is_import_from_piper_source_code = "__file__" in globals and "piper/" in globals["__file__"]
    not_piper_import = not ("piper" in name)
    result = is_import_from_piper_source_code and not_piper_import

    return result


def try_import(name, globals={}, locals={}, fromlist=[], level=0):
    """
    This import replace real Python import with fake import which returns warning only and PiperDummyModule.
    This works for everything under piper/ frameworks files by filename but not for piper import (like piper.base)
    And this also works for every file where you import something from piper firstly !
    """
    if not (configuration.ignore_import_errors or configuration.safe_import_activated):
        logger.info("Ignore import errors is off in Configuration and deactivated")
        return real_import(name, globals, locals, fromlist, level)

    piper_was_touched_in_previous_frame = _piper_was_touched_in_frame(frame_before=1)
    need_to_catch = piper_was_touched_in_previous_frame or _from_piper_file_but_not_piper(name, globals)

    if need_to_catch:
        logger.info(f"Piper runs safe import for library {name} in piper file {globals['__file__']} ")
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


def _set_import_functions(ignore: bool = True):
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
    configuration.safe_import_activated = True
    _set_import_functions(ignore=True)


def deactivate_safe_import():
    logger.info(f"Piper deactivates safe import")
    configuration.safe_import_activated = False
    _set_import_functions(ignore=configuration.ignore_import_errors)


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
