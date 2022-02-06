import os
import sys
root_dir = os.path.join(os.path.realpath(os.path.pardir), 'piper')
sys.path.insert(1, root_dir)

from piper.utils import docker_utils as du
from piper.envs import CurrentEnv

def test_start_container():
    with CurrentEnv() as env:
        print(env)
    assert True == True

# du.get_container('asba', 'dkfja')


import os

def test_dummy():
    print(f'file {os.path.dirname(__file__)}')
    print(f'name', os.path.dirname(__name__))
    assert True == True