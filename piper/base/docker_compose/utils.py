import os

import jinja2

from piper.utils.logger_utils import logger


class ComposeServices:

    def __init__(
            self,
            name_path: str,
    ):
        self.name_path = name_path

    @staticmethod
    def render_script_fastapi():
        """
        Render main file for virtual env logic
        """
        logger.info('Render main file for fastapi in compose services')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('python-script-fastapi.j2')
        return template.render()

    def render_bash_start(self):
        """
        Render bash script for create and activate venv
        """
        logger.info('Render bash script for create and activate venv')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('bash-start-compose.j2')
        return template.render(
            name_path=self.name_path,
        )

    def render_bash_stop(self):
        """
        Render main file for virtual env logic
        """
        logger.info('Render main file for virtual env logic')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('bash-stop-compose.j2')
        return template.render(
            name_path=self.name_path,
        )

    @staticmethod
    def render_compose_services():
        """
        Render bash script for create and activate venv
        """
        logger.info('Render bash script for create and activate venv')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('compose-services.j2')
        return template.render()

    @staticmethod
    def render_dockerfile():
        """
        Render bash script for create and activate venv
        """
        logger.info('Render bash script for create and activate venv')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('dockerfile.j2')
        return template.render()
