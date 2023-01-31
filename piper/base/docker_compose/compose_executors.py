import inspect
import subprocess
from typing import Dict

from piper.base.docker_compose.utils import ComposeServices
from piper.configurations import get_configuration
from piper.utils.logger_utils import logger


def copy_piper(path: str):
    cfg = get_configuration()
    from distutils.dir_util import copy_tree
    copy_tree(cfg.piper_path, f"{path}/piper")


def copy_scripts(path: str, scripts: Dict[str, str]):
    for script_name, script_path in scripts.items():
        with open(f"{path}/{script_name}.py", "w") as output:
            with open(script_path, "r") as current_file:
                output.write(current_file.read())


def write_requirements(path, requirements):
    with open(f"{path}/requirements.txt", "w") as output:
        output.write("\n".join(requirements))


class ComposeExecutor:
    requirements = ["gunicorn", "fastapi", "uvicorn", "aiohttp",
                    "Jinja2", "pydantic", "pymilvus", "numpy", "loguru"]

    def __init__(self):
        logger.info('ComposeExecutor init with is_compose_env()')

        cfg = get_configuration()
        self.project_output_path = cfg.path

    def scripts(self):
        return {"service": inspect.getfile(self.__class__)}

    def copy_struct_project(self):
        copy_piper(self.project_output_path)
        copy_scripts(self.project_output_path, self.scripts())

    def create_files_for_compose(self, testing: bool = False):
        logger.info('ComposeExecutor create_fast_api_files_venv()')

        compose_service = ComposeServices(
            name_path=self.project_output_path,
        )

        main_fastapi = compose_service.render_script_fastapi()
        with open(f"{self.project_output_path}/main.py", "w") as output:
            output.write(main_fastapi)

        docker_compose = compose_service.render_compose_services()
        with open(f"{self.project_output_path}/docker-compose.yaml", "w") as output:
            output.write(docker_compose)

        bash_start = compose_service.render_bash_start(testing=testing)
        with open(f"{self.project_output_path}/bash-start.sh", "w") as output:
            output.write(bash_start)

        bash_stop = compose_service.render_bash_stop()
        with open(f"{self.project_output_path}/bash-stop.sh", "w") as output:
            output.write(bash_stop)

        dockerfile = compose_service.render_dockerfile()
        with open(f"{self.project_output_path}/Dockerfile", "w") as output:
            output.write(dockerfile)

        write_requirements(self.project_output_path, self.requirements)

    def start_compose(self):
        process_chmod_start = subprocess.run(f'chmod +x {self.project_output_path}bash-start.sh', shell=True)
        process_run = subprocess.run(f'{self.project_output_path}bash-start.sh', shell=True)

    def stop_compose(self):
        process_chmod_stop = subprocess.run(f'chmod +x {self.project_output_path}bash-stop.sh', shell=True)
        process_run = subprocess.run(f'{self.project_output_path}bash-stop.sh', shell=True)
