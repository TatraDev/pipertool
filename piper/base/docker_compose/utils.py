from piper.configurations import get_configuration
from piper.base.rendering import Render

cfg = get_configuration()


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
        python_fastapi_milvus_render = Render('python-fastapi-milvus.j2')
        return python_fastapi_milvus_render.render()

    def render_bash_start(self, testing: bool = False):
        """
        Render bash script for bash_start
        """
        bash_start_compose = Render('bash-start-compose.j2')

        compose_flag = '' if testing else '-d'
        return bash_start_compose.render(
            name_path=self.name_path,
            compose_flag=compose_flag,
        )

    def render_bash_stop(self):
        """
        Render bash script for bash_stop
        """
        bash_stop_compose_render = Render('bash-stop-compose.j2')
        return bash_stop_compose_render.render(
            name_path=self.name_path,
        )

    @staticmethod
    def render_compose_services():
        """
        Render script for compose_services
        """
        compose_services_render = Render('compose-services.j2')
        return compose_services_render.render()

    @staticmethod
    def render_dockerfile():
        """
        Render dockerfile
        """
        dockerfile_render = Render('dockerfile.j2')
        return dockerfile_render.render()
