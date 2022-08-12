import inspect
import os
import subprocess
from typing import Dict

from piper.base.virtualenv.utils import VenvPython
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


class VirtualEnvExecutor:
    requirements = ["gunicorn", "fastapi", "uvicorn", "aiohttp", "docker", "Jinja2", "pydantic", "loguru"]

    def __init__(self):
        logger.info('VirtualEnvExecutor init with is_virtual_env()')

        cfg = get_configuration()
        self.project_output_path = cfg.path
        self.name_venv = cfg.name_venv
        self.number = cfg.number

    def scripts(self):
        return {"service": inspect.getfile(self.__class__)}

    def copy_struct_project(self):
        copy_piper(self.project_output_path)
        copy_scripts(self.project_output_path, self.scripts())

    def create_files_for_venv(self):
        logger.info('VirtualEnvExecutor create_fast_api_files_venv()')

        venv_python_image = VenvPython(
            name_path=self.project_output_path,
            name_venv=self.name_venv,
            number=self.number,
        )

        venv_main = venv_python_image.render_venv_python()
        with open(f"{self.project_output_path}/main.py", "w") as output:
            output.write(venv_main)

        venv_bash = venv_python_image.render_venv_bash()
        with open(f"{self.project_output_path}/create_venv.sh", "w") as output:
            output.write(venv_bash)

        write_requirements(self.project_output_path, self.requirements)

        process_chmod = subprocess.run(f'chmod +x {self.project_output_path}create_venv.sh', shell=True)
        process_run = subprocess.run(f'{self.project_output_path}create_venv.sh', shell=True)

    def create_files_for_tests(self):
        logger.info('VirtualEnvExecutor create_files_for_tests()')

        with open(f"{self.project_output_path}/__init__.py", "w") as output:
            pass

        tests_directory = f"{self.project_output_path}/tests"
        if not os.path.exists(tests_directory):
            os.makedirs(tests_directory)

        with open(f"{self.project_output_path}/tests/__init__.py", "w") as output:
            pass

        venv_python_image = VenvPython(
            name_path=self.project_output_path,
            name_venv=self.name_venv,
            number=self.number,
        )

        test_main = venv_python_image.render_tests_python()
        with open(f"{self.project_output_path}/tests/test_main.py", "w") as output:
            output.write(test_main)

        test_bash = venv_python_image.render_tests_bash()
        with open(f"{self.project_output_path}/test_venv.sh", "w") as output:
            output.write(test_bash)
