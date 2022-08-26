import asyncio
import os
import sys

import docker

root_dir = os.path.join(os.path.realpath(os.path.pardir), 'piper')
sys.path.insert(1, root_dir)

from piper.base.executors import copy_piper, copy_scripts
from piper.configurations import get_configuration
from piper.envs import CurrentEnv, is_docker_env
from piper.services import StringValue, TestMessageAdder
from piper.utils import docker_utils as du


def test_start_container():
    cfg = get_configuration()
    loop = asyncio.get_event_loop()
    init_value = "TEST_container_"
    x = StringValue(value=init_value)
    need_result = f'{init_value}TEST'
    adder = TestMessageAdder(appender="!", port=cfg.docker_app_port)
    result = loop.run_until_complete(adder(x))
    print(result)
    adder.rm_container()

    assert result.get('value') == need_result
