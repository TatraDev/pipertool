import jinja2

from piper.utils.logger_utils import logger
from piper.configurations import get_configuration

cfg = get_configuration()


class Render:

    def __init__(self, template_file: str):
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(cfg.templates_path),
                                            trim_blocks=True,
                                            lstrip_blocks=True)
        self.template_file = template_file
        self.template = self.jinja_env.get_template(template_file)

    def render(self, **kwargs):
        logger.info(f'Render {self.template_file} with {kwargs}')
        return self.template.render(**kwargs)
