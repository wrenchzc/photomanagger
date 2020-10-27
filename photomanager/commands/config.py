import os
from photomanager.lib.pmconst import PATH_SEP
from photomanager.commands.base import Command
from photomanager.db.config import FieldBackupDir
from photomanager.utils.pathutils import is_abspath


class CommandConfig(Command):

    def do(self):
        for key in self.params:
            value = self.params[key]
            if self._before_set_value(key, value):
                self.config.set_value(key, value)

    def _before_set_value(self, key, value):
        if key == FieldBackupDir:
            return self._do_before_set_backup_dir(value)

    def _do_before_set_backup_dir(self, value):
        path = value
        if not is_abspath(value):
            path = f"{self.folder}{PATH_SEP}{value}"

        return os.makedirs(path, exist_ok=True)
