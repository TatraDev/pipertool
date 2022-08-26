import os

import jinja2

from piper.utils.logger_utils import logger


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
        logger.info('Render bash script for create and activate venv')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('bash-create-venv.j2')
        return template.render(
            name_path=self.name_path,
            name_venv=self.name_venv,
            number=self.number,
        )

    @staticmethod
    def render_venv_python():
        """
        Render main file for virtual env logic
        """
        logger.info('Render main file for virtual env logic')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('python-script-venv.j2')
        return template.render()

    def render_tests_bash(self):
        """
        Render bash script for create and activate venv
        """
        logger.info('Render bash script for create and activate venv')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('bash-create-tests.j2')
        return template.render(
            name_venv=self.name_venv,
        )

    def render_tests_python(self):
        """
        Render bash script for create and activate venv
        """
        logger.info('Render bash script for create and activate venv')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('python-script-tests.j2')
        return template.render(
            number=self.number,
        )
