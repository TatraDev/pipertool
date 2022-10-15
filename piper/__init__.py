from piper.configurations import get_configuration
from piper.imports import activate_safe_import

configuration = get_configuration()
if configuration.ignore_import_errors:
    """
    Piper activates safe import if configured True.
    This ignores any import errors for safe imports in piper.base.executors
    """
    activate_safe_import()
