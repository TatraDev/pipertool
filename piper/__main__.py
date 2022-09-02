import os
import sys

import click

root_dir = os.path.join(os.path.realpath(os.path.pardir), '.')
sys.path.insert(1, root_dir)

from piper.envs import ComposeEnv

# def main():
#     with ComposeEnv() as env:
#         try:
#             env.copy_struct_project()
#             env.create_files_for_compose()
#             env.start_compose()
#         except KeyboardInterrupt:
#             logger.info('Ctrl+C pressed. Except KeyboardInterrupt.')
#             env.stop_compose()
#             sys.exit(1)
#


@click.command()
@click.argument('type_command')
@click.option(
    '--env-type', '-e',
    help='your current interpretation',
)
def main(type_command: str, env_type: str):
    if env_type == 'compose':
        if type_command == 'start':
            print("type_command == 'start'")
            with ComposeEnv() as env:
                env.copy_struct_project()
                env.create_files_for_compose()
                env.start_compose()
        elif type_command == 'stop':
            print("type_command == 'stop'")
            with ComposeEnv() as env:
                env.stop_compose()
    else:
        raise NotImplementedError(f'{env_type} not released in this version pipertool')


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("CVE")
    main()
