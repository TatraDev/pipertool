from piper.configurations import get_configuration
from piper.base.rendering import Render

cfg = get_configuration()


class PythonImage:

    def __init__(self,
                 tag: str,
                 python_docker_version: str,
                 cmd: str,
                 template_file: str,
                 run_rows,
                 post_install_lines):
        self.tag = tag
        self.python_docker_version = python_docker_version
        self.cmd = cmd
        self.template_file = template_file
        self.run_rows = run_rows
        self.post_install_lines = post_install_lines
        self._render = Render(template_file)

    def render(self):
        """
        Render docker template
        """
        return self._render.render(cmd=self.cmd,
                                   python_docker_version=self.python_docker_version,
                                   run_command_lines=self.run_rows,
                                   post_install_lines=self.post_install_lines)

# class PythonTesseractImage:

#     def __init__(self, tag, python_docker_version, cmd):
#         self.tag = tag
#         self.python_docker_version = python_docker_version
#         self.cmd = cmd


#     def render(self):
#         """
#         Render docker template
#         """
#         template_dir = os.path.join(os.path.dirname(__file__), 'images')
#         jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
#                                        trim_blocks=True,
#                                        lstrip_blocks=True)
#         template = jinja_env.get_template('python-tesrct.j2')
#         return template.render(cmd=self.cmd, python_docker_version=self.python_docker_version, run_command_lines=self.run_command_lines)
