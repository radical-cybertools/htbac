import logging
import parmed as pmd

from .abpath import AbFolder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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

        self.box_x, self.box_y, self.box_z = pmd.amber.AmberAsciiRestart(self.coordinate.path).box[:3]

        if 'constraint' in [f.tag for f in files]:
            df = pmd.load_file(self.constraint.path).to_dataframe()
            all_o_same = all(df.occupancy.values == df.occupancy.values[0])
            all_b_same = all(df.bfactor.values == df.bfactor.values[0])

            if all_o_same and not all_b_same:
                self.constraint_column = 'B'
            elif all_b_same and not all_o_same:
                self.constraint_column = 'O'
            else:
                raise ValueError('Invalid constraint file!')

            logger.info('Constraint column set to: {}'.format(self.constraint_column))

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
            return next(f for f in self._files if f.tag == item)
        except StopIteration:
            raise AttributeError("'System' object has no attribute {}".format(item))
