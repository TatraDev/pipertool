from piper.configurations import get_configuration
from piper.imports import _set_import_functions

configuration = get_configuration()

if configuration.ignore_import_errors:
    """
    Piper activates safe import globally for piper work if configured True.
    This ignores any import errors for safe imports in piper.base.executors
    """
    _set_import_functions(ignore=True)
