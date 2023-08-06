
from logging import Logger
from logging import getLogger

from click import secho

from buildlackey.Environment import Environment


class RunMypy(Environment):
    
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def execute(self):
        self._changeToProjectRoot()

        # noinspection SpellCheckingInspection
        cmd: str = f'mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes --check-untyped-defs  {self._projectDirectory} tests'
        secho(f'{cmd}')

        status: int = self._runCommand(command=cmd)
        secho(f'{status=}')
