import os
import parmed as pmd


class System(object):

    def __init__(self, prefix):
        self.prefix = prefix
        self.box = pmd.amber.AmberAsciiRestart(prefix + '-complex.inpcrd').box

    @property
    def name(self):
        return os.path.basename(self.prefix)

    # TODO: instead create a specific systems loader that read in systems with this type of folder setup.
    _suffixes = ['-complex.inpcrd', '-complex.pdb', '-complex.top', '-cons.pdb']

    def file_paths(self, relative_to=None):
        if relative_to:
            return [os.path.join(relative_to, (self.name+suffix)) for suffix in self._suffixes]
        else:
            return [self.prefix + suffix for suffix in self._suffixes]

    @property
    def shared_data(self):
        return [self.prefix + suffix for suffix in self._suffixes]

    @property
    def water_model(self):
        # TODO: read in water model from structure file. Look at WAT ot HOH.
        return NotImplemented

    def __repr__(self):
        return self.name

    @classmethod
    def from_hyphen_separated_name(cls, name, rootdir):
        comps = [os.path.abspath(rootdir)] + name.split('-') + [name]
        prefix = os.path.join(*comps)
        return System(prefix)
