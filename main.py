import sys

from loguru import logger

from piper.envs import ComposeEnv

logger.add("file.log", level="INFO", backtrace=True, diagnose=True, rotation='5 MB')

if __name__ == '__main__':
    with ComposeEnv() as env:
        try:
            env.copy_struct_project()
            env.create_files_for_compose()
            env.start_compose()
        except KeyboardInterrupt:
            logger.info('Ctrl+C pressed. Except KeyboardInterrupt.')
            env.stop_compose()
            sys.exit(1)
