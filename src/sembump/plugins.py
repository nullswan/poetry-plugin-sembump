from poetry.console.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin

from sembump.commands import BumpCommand


class SembumpPlugin(ApplicationPlugin):
    @property
    def commands(self) -> list[type[Command]]:
        return [BumpCommand]
