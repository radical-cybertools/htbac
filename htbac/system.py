import os
from shutil import copyfile

import parmed as pmd

from .abpath import AbFolder, AbFile


class System(AbFolder):
    """ Object describing a molecular system to be simulated.

    `System` is a container storing all the files required to run a certain molecular system. It also defines a
    number of convenience methods to load systems with certain folder structures, and attributes that are required
    as input to MD engine configuration files.

    """
    def __init__(self, name, files):
        """An object containing references to files that make up the system. There are some
        methods on it for convenience like box vector or water model.

        Parameters
        ----------
        name: str
        files: list
            AbFiles with tags one of [coordinate, pdb, topology, alchemical_path, constraint, restraint]
        """

        AbFolder.__init__(self)

        self.name = name

        self._files = files

        self.box_x, self.box_y, self.box_z = pmd.amber.AmberAsciiRestart(self.files['coordinate']).box

    @classmethod
    def with_common_prefix(cls, name, common_prefix, add_prefix=False):
        """Load a system with a give prefix

        Parameters
        ----------
        common_prefix: str
            Truncated path to the system.
        add_prefix: bool
        Returns
        -------
            System
        """

        return System(name=name, pdb=prefix+'-complex.pdb', coordinate=prefix+'-complex.inpcrd',
                      topology=prefix+'-complex.top', constraints=prefix+'-cons.pdb',
                      alchemical_tags=prefix+'-tags.pdb', add_prefix=add_prefix)

    @classmethod
    def from_hyphen_separated_name(cls, name, rootdir):
        """

        Parameters
        ----------
        name: str
            Hyphen separated name of the system. The components will be assumed to be the names of the directory
            it is contained in. For example `nilotinib-e255k` should to be in the folder `rootdir/nilotinib/e255k/`.
        rootdir: str
            The root directory where to look for the files.

        Returns
        -------
        System
            A new instance of `System` with the files correctly loaded in.

        """
        comps = [rootdir] + name.split('-') + [name]
        prefix = os.path.join(*comps)
        return System.with_prefix(prefix)

    @property
    def water_model(self):
        """The water model of the system. Can be one of `tip3`, `tip4`.

        Returns
        -------
        str

        """
        # TODO: read in water model from structure file. Look at WAT ot HOH.
        return NotImplemented

    def __repr__(self):
        return self.name

    def __getattr__(self, item):
        try:
            return next(f.name for f in self._files if f.tag == item)
        except KeyError:
            raise AttributeError('System has no attribute {}'.format(item))
