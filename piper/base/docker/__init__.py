import os
import jinja2


class PythonImage:

    def __init__(self, tag, python_docker_version, cmd):
        self.tag = tag
        self.python_docker_version = python_docker_version
        self.cmd = cmd

    def render(self):
        """
        Render docker template
        """
        template_dir = os.path.join(os.path.dirname(__file__), 'images')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('default-python.j2')
        return template.render(cmd=self.cmd, python_docker_version=self.python_docker_version)


class PythonTsrImage:

    def __init__(self, tag, python_docker_version, cmd):
        self.tag = tag
        self.python_docker_version = python_docker_version
        self.cmd = cmd

    def render(self):
        """
        Render docker template
        """
        template_dir = os.path.join(os.path.dirname(__file__), 'images')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template('python-tesrct.j2')
        return template.render(cmd=self.cmd, python_docker_version=self.python_docker_version)