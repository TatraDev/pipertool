from piper.configurations import get_configuration
from piper.base.rendering import Render

cfg = get_configuration()


class VenvPython:

    def __init__(
            self,
            name_path: str,
            name_venv: str,
            number: int,
    ):
        self.name_path = name_path
        self.name_venv = name_venv
        self.number = number

    def render_venv_bash(self):
        """
        Render bash script for create and activate venv
        """
        venv_bash_render = Render('bash-create-venv.j2')
        return venv_bash_render.render(
            name_path=self.name_path,
            name_venv=self.name_venv,
            number=self.number,
        )

    @staticmethod
    def render_venv_python():
        """
        Render main file for virtual env logic
        """
        venv_python_render = Render('python-script-venv.j2')
        return venv_python_render.render()

    def render_tests_bash(self):
        """
        Render bash script for create and activate venv
        """
        bash_create_render = Render('bash-create-tests.j2')
        return bash_create_render.render(
            name_venv=self.name_venv,
        )

    def render_tests_python(self):
        """
        Render bash script for create and activate venv
        """
        python_tests_render = Render('python-script-tests.j2')
        return python_tests_render.render(
            number=self.number,
        )
