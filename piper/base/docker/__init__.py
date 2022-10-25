import os

import jinja2


class PythonImage:

    def __init__(self, tag, python_docker_version, cmd, template_file, run_rows, post_install_lines):
        self.tag = tag
        self.python_docker_version = python_docker_version
        self.cmd = cmd
        self.template_file = template_file
        self.run_rows = run_rows
        self.post_install_lines = post_install_lines

    def render(self):
        """
        Render docker template
        """
        template_dir = os.path.join(os.path.dirname(__file__), 'images')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template(self.template_file)
        return template.render(cmd=self.cmd,
                               python_docker_version=self.python_docker_version,
                               run_command_lines=self.run_rows,
                               post_install_lines=self.post_install_lines)


class TensorFlowImage:

    def __init__(self, tag, python_docker_version, cmd, template_file, run_rows, post_install_lines):
        self.tag = tag
        self.python_docker_version = python_docker_version
        self.cmd = cmd
        self.template_file = template_file
        self.run_rows = run_rows
        self.post_install_lines = post_install_lines

    def render(self):
        """
        Render docker template
        """
        template_dir = os.path.join(os.path.dirname(__file__), 'images')
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       trim_blocks=True,
                                       lstrip_blocks=True)
        template = jinja_env.get_template(self.template_file)
        return template.render(cmd=self.cmd, ddocker_name=self.tag, ddocker_version=self.python_docker_version, run_command_lines=self.run_rows, post_install_lines=self.post_install_lines)

