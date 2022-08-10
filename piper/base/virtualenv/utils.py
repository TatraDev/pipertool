import os

import jinja2

from piper.utils.logger_utils import logger


class VenvPythonImage:

    def __init__(
            self,
            name_path: str,
            name_venv: str,
            api_host: str,
            api_port: int,
    ):
        self.name_path = name_path
        self.name_venv = name_venv
        self.api_host = api_host
        self.api_port = api_port

    def render_venv_bash(self):
        """
        Render bash script for create and activate venv
        """
        logger.info('Render bash script for create and activate venv')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('default-venv.j2')
        return template.render(
            name_path=self.name_path,
            name_venv=self.name_venv,
            api_host=self.api_host,
            api_port=self.api_port,
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
        template = jinja_env.get_template('python-venv.j2')
        return template.render()
