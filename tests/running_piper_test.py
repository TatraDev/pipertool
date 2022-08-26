# pytest -vs tests/running_piper_test.py::TestDocker
import requests

main_app_url = f'http://localhost:8788'

class TestDocker():
    '''
        Docker container API test. Methods:
            health_check
            run
    '''
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


class TestVenv():
    '''
        venv container API test. Methods:
            dummy
    '''
    def test_dummy(self):
        assert 1 / 0