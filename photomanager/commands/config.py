import os
from photomanager.commands.base import Command
from photomanager.db.config import FieldBackupDir


class CommandConfig(Command):

    def do(self):
        for key in self.params:
            value = self.params[key]
            if self._before_set_value(key, value):
                self.config.set_value(key, value)

    def _before_set_value(self, key, value):
        if key == FieldBackupDir:
            return self._do_before_set_backup_dir()

    @staticmethod
    def _do_before_set_backup_dir(value):
        return os.makedirs(value, exist_ok=True)
