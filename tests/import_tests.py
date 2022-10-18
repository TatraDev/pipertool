import pytest


class TestSafeImport:

    def test_safe_import_after_piper(self):
        import piper
        import foo
        from piper.imports import PiperDummyModule
        assert isinstance(foo, (PiperDummyModule, ))

    def test_safe_import_before_piper(self):
        # it doesn't work normally
        with pytest.raises(ImportError):
            import foo
            import piper

    def test_safe_import_after_executors_import(self):
        from piper.base import executors
        import foo
        from piper.imports import PiperDummyModule
        assert isinstance(foo, (PiperDummyModule, ))

    def test_safe_import_after_base_executor(self):
        from piper.base.executors import BaseExecutor
        import foo
        from piper.imports import PiperDummyModule
        assert isinstance(foo, (PiperDummyModule, ))

    def test_safe_import_after_piper_as_p(self):
        import piper as p
        import foo
        from piper.imports import PiperDummyModule
        assert isinstance(foo, (PiperDummyModule,))

    def test_not_ignore_error_by_flag(self):
        import piper as p
        p.configurations.Configuration.ignore_import_errors = False
        with pytest.raises(ImportError):
            import foo

    def test_safe_import_as_context_when_global_off(self):
        import piper as p
        p.configurations.Configuration.ignore_import_errors = False
        with p.imports.safe_import():
            import foo
            from piper.imports import PiperDummyModule
            assert isinstance(foo, (PiperDummyModule,))
        # safe import was deactivated
        with pytest.raises(ImportError):
            import bar

    def test_safe_import_as_context_when_global_on(self):
        import piper as p
        p.configurations.Configuration.ignore_import_errors = True
        with p.imports.safe_import():
            import foo
            from piper.imports import PiperDummyModule
            assert isinstance(foo, (PiperDummyModule,))
        # safe import was deactivated but global is on
        import bar
        assert isinstance(bar, (PiperDummyModule,))