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
        Render main file for fastapi
        """
        logger.info('Render main file for fastapi in compose services')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('python-fastapi-milvus.j2')
        return template.render()

    def render_bash_start(self, testing: bool = False):
        """
        Render bash script for bash_start
        """
        logger.info('Render bash script for bash_start')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('bash-start-compose.j2')

        compose_flag = '' if testing else '-d'
        return template.render(
            name_path=self.name_path,
            compose_flag=compose_flag,
        )

    def render_bash_stop(self):
        """
        Render bash script for bash_stop
        """
        logger.info('Render bash script for bash_stop')

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
        Render script for compose_services
        """
        logger.info('Render script for compose_services')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('compose-services.j2')
        return template.render()

    @staticmethod
    def render_dockerfile():
        """
        Render dockerfile
        """
        logger.info('Render dockerfile')

        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('dockerfile.j2')
        return template.render()
