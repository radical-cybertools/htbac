from pathlib2 import Path


class AbFile(Path):
    """An protocol for objects that support RP style path mechanism.

    RP has a somewhat complicated way to assign path to files based on a number of factors.
    The same file has path on local, path on remote shared, path on remote inside a unit.
    Not just that but inside units, files can be copied or linked based on whether they will
    be edited inside a unit or not. It is complicated, and this protocol tries to take care of
    this.
    """

    def __init__(self, path, tag=str(), needs_copying=False, is_executable_argument=False):

        self.tag = tag
        self.needs_copying = needs_copying
        self.is_executable_argument = is_executable_argument

        super(AbFile, self).__init__(path)

    @property
    def remote_shared_path(self):
        return Path('$SHARED', self.name)

    def with_prefix(self, prefix):
        self.rename(prefix+self.name)

        new_file = self.with_name(prefix+self.name)
        new_file.tag = self.tag
        new_file.needs_copying = self.needs_copying
        new_file.is_executable_argument = self.is_executable_argument
        return new_file


class AbFolder:

    def __init__(self):

        self._files = list()

    @property
    def shared_files(self):
        return self._files

    @property
    def arguments(self):
        return [f.name for f in self._files if f.is_executable_argument]

    @property
    def copied_files(self):
        return [f.remote_shared_path for f in self._files if f.needs_copying]

    @property
    def linked_files(self):
        return [f.remote_shared_path for f in self._files if not f.needs_copying]

