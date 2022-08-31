# pytest -vs tests/running_piper_test.py::TestDocker
import time
from pathlib import Path
from shlex import split
from subprocess import check_call
from tempfile import TemporaryDirectory
from venv import create

import requests

from piper.envs import VirtualEnv, ComposeEnv

main_app_url = f'http://localhost:8788'


class TestDocker:
    """
        Docker container API test. Methods:
            health_check
            run
    """

    def test_health_check(self):
        url = f'{main_app_url}/health_check'
        print(url)
        result = requests.post(url)
        assert result.status_code == 200

    def test_run(self):
        url = f'{main_app_url}/run'
        print(url)
        data = {'value': 'hello, world'}
        response = requests.post(url, json=data)
        result = dict(response.json())
        need_result = f"{data.get('value')}TEST"
        print(f'need_result is {need_result}')
        print(f"docker result is {result.get('value')}")

        assert response.status_code == 200
        assert need_result == result.get('value')


class TestVenv:
    """
        venv test. Methods:
            scenario
    """

    def test_scenario(self):
        with VirtualEnv() as env:
            env.copy_struct_project()
            env.create_files_for_venv()
            env.create_files_for_tests()


class TestCompose:
    """
        Compose test. Methods:
            scenario
    """

    def test_health_check(self):
        with ComposeEnv() as compose:
            compose.copy_struct_project()
            compose.create_files_for_compose()
            compose.start_compose()

            time.sleep(5)
            url = 'http://127.0.0.1:7585/health_check'
            result = requests.get(url)
            assert result.status_code == 200

            compose.stop_compose()

