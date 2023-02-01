from piper.base.backend import utils
from piper.base.rendering.meta import ExecutorMetaInfo, Function, FunctionArg


class TestRenders:

    def test_fastapi_utils(self):
        meta_info = ExecutorMetaInfo(
            class_name="CustomExecutor",
            init_kwargs={'config_a': 0., 'config_b': {"inner": 0}},
            scripts={"service": "piper.services.CustomExecutor"},
            async_functions=[Function(name="run",
                                      input_args=[FunctionArg("request_model", "StringValue")])]
        )

        result = utils.render_fast_api_backend(meta_info)

        print(result)
