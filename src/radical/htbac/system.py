import os
import parmed as pmd


class System(object):

    def __init__(self, prefix):
        self.prefix = prefix
        self.box = pmd.amber.AmberAsciiRestart(prefix + '-complex.inpcrd').box

    @property
    def name(self):
        return os.path.basename(self.prefix)

    _suffixes = ['-complex.inpcrd', '-complex.pdb', '-complex.top', '-cons.pdb']

    def file_paths(self, relative_to=None):
        if relative_to:
            return [os.path.join(relative_to, (self.name+suffix)) for suffix in self._suffixes]
        else:
            return [self.prefix + suffix for suffix in self._suffixes]

    @property
    def shared_data(self):
        return [self.prefix + suffix for suffix in self._suffixes]

