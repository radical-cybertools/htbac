import parmed as pmd

import radical.utils as ru

from .abpath import AbFolder

logger = ru.Logger(__name__, level='DEBUG')


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

        self._constraint_column = None

    @property
    def water_model(self):
        """The water model of the system. Can be one of `tip3`, `tip4`.

        Returns
        -------
        str

        """
        # TODO: read in water model from structure file. Look at WAT ot HOH.
        return NotImplemented

    @property
    def constraint_column(self):
        if self._constraint_column is None:
            df = pmd.load_file(self.constraint.path).to_dataframe()
            all_o_same = all(df.occupancy.values == df.occupancy.values[0])
            all_b_same = all(df.bfactor.values == df.bfactor.values[0])

            if all_o_same and not all_b_same:
                self._constraint_column = 'B'
            elif all_b_same and not all_o_same:
                self._constraint_column = 'O'
            else:
                raise ValueError('Invalid constraint file!')

            logger.info('Constraint column set to: {}'.format(self.constraint_column))

        return self._constraint_column

    @constraint_column.setter
    def constraint_column(self, value):
        self._constraint_column = value

    def __repr__(self):
        return self.name

    def __getattr__(self, item):
        try:
            return next(f for f in self._files if f.tag == item)
        except StopIteration:
            raise AttributeError("System {} has no `{}`".format(self.name, item))
