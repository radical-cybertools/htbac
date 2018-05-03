import os
import parmed as pmd


class System(object):
    """ Object describing a molecular system to be simulated.

    `System` is a container storing all the files required to run a certain molecular system. It also defines a
    number of convenience methods to load systems with certain folder structures, and attributes that are required
    as input to MD engine configuration files.

    """
    def __init__(self, name, pdb, coordinate, topology, constraints=None, alchemical_tags=None):
        """An object containing references to files that make up the system. There are some
        methods on it for convenience like box vector or water model.

        Parameters
        ----------
        name: str
        pdb: str
        coordinate: str
        topology: str
        constraints: str
        alchemical_tags: str
        """

        self.name = name
        self.pdb = pdb
        self.coordinate = coordinate
        self.topology = topology
        self.constraints = constraints
        self.alchemical_tags = alchemical_tags

        self.box = pmd.amber.AmberAsciiRestart(coordinate).box

    @classmethod
    def with_prefix(cls, prefix):
        """Load a system with a give prefix

        Parameters
        ----------
        prefix: str
            Truncated path to the system.
        Returns
        -------
            System
        """

        name = os.path.basename(prefix)

        return System(name=name, pdb=prefix+'-complex.pdb', coordinate=prefix+'-complex.inpcrd',
                      topology=prefix+'-complex.top', constraints=prefix+'-cons.pdb',
                      alchemical_tags=prefix+'-tags.pdb')

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

    _suffixes = ['-complex.inpcrd', '-complex.pdb', '-complex.top', '-cons.pdb']

    @property
    def input_files(self):
        """
        List of the names of the files. This is just the name, not the path.
        """
        return [os.path.basename(f) for f in self.shared_data]

    @property
    def shared_data(self):
        """

        List of paths to all the files needed to describe the system.

        """
        return filter(None, [self.pdb, self.coordinate, self.topology, self.constraints, self.alchemical_tags])

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
