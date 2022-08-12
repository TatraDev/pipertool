from piper.envs import VirtualEnv

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     with VirtualEnv() as env:
#         x = StringValue(value="hello, world")
#         adder = TestMessageAdder(appender="!", port=8788)
#         result = loop.run_until_complete(adder(x))
#         print(result)
#
#     x = StringValue(value="hello, world")
#     adder = TestMessageAdder(appender="!", port=8788)
#     result = loop.run_until_complete(adder(x))
#     print(result)
#     adder.rm_container()

if __name__ == '__main__':
    with VirtualEnv() as env:
        env.copy_struct_project()
        env.create_files_for_venv()
        env.create_files_for_tests()
