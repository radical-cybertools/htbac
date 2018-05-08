import os
import shutil
import filecmp


class AbFile:
    """An protocol for objects that support RP style path mechanism.

    RP has a somewhat complicated way to assign path to files based on a number of factors.
    The same file has path on local, path on remote shared, path on remote inside a unit.
    Not just that but inside units, files can be copied or linked based on whether they will
    be edited inside a unit or not. It is complicated, and this protocol tries to take care of
    this.
    """

    def __init__(self, path, tag=str(), needs_copying=False, is_executable_argument=False):

        self.path = path
        self.tag = tag
        self.needs_copying = needs_copying
        self.is_executable_argument = is_executable_argument

    @property
    def remote_shared_path(self):
        return os.path.join('$SHARED', self.name)

    @property
    def name(self):
        return os.path.basename(self.path)

    def __repr__(self):
        return self.name

    def with_prefix(self, prefix):

        head, tail = os.path.split(self.path)
        new_path = os.path.join(head, prefix+'-'+tail)
        if not os.path.exists(new_path) or not filecmp.cmp(self.path, new_path):
            shutil.copyfile(self.path, new_path)

        self.path = new_path
        return self


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

