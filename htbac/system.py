import os
import parmed as pmd


class System(object):
    """ Object describing a molecular system to be simulated.

    `System` is a container storing all the files required to run a certain molecular system. It also defines a
    number of convenience methods to load systems with certain folder structures, and attributes that are required
    as input to MD engine configuration files.

    """
    def __init__(self, prefix):
        """

        Parameters
        ----------
        prefix: str
                Prefix of the system files. All sub-files (coordinate, topology) must have this prefix. They
                are automatically loaded into the object.
        """

        self.prefix = prefix
        self.box = pmd.amber.AmberAsciiRestart(prefix + '-complex.inpcrd').box

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
        comps = [os.path.abspath(rootdir)] + name.split('-') + [name]
        prefix = os.path.join(*comps)
        return System(prefix)

    @property
    def name(self):
        """

        Returns
        -------
        str
            The name of the system. That is the name of the files without the common suffixes.
        """
        return os.path.basename(self.prefix)

    # TODO: instead create a specific systems loader that reads in systems with this type of folder setup.
    _suffixes = ['-complex.inpcrd', '-complex.pdb', '-complex.top', '-cons.pdb']

    def file_paths(self, relative_to=None):
        """

        Parameters
        ----------
        relative_to: str
            Return the file paths of the system relative to this path.

        Returns
        -------
        list
            List of file paths of all the system files.

        """
        if relative_to:
            return [os.path.join(relative_to, (self.name+suffix)) for suffix in self._suffixes]
        else:
            return [self.prefix + suffix for suffix in self._suffixes]

    @property
    def shared_data(self):
        return [self.prefix + suffix for suffix in self._suffixes]

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
